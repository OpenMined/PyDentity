import asyncio
from aries_basic_controller.aries_controller import AriesAgentController
import json

import torch

# models
from torch import nn
from torch import optim
from torch.autograd import Variable
import os
import sys

from opacus import PrivacyEngine

# The Researcher generates the model

# Data pre-processing

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

# prep
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.datasets import make_classification
from sklearn.preprocessing import binarize, LabelEncoder, MinMaxScaler
from sklearn import metrics



import time


class Researcher:
    
    def __init__(self, agent_config, validation_data_path, model):
        
        self.agent_controller = AriesAgentController(webhook_host=agent_config["webhook_host"],webhook_port=agent_config["webhook_port"],                                       webhook_base=agent_config["webhook_base"], admin_url=agent_config["admin_url"])
        
        self._register_agent_listeners()
        
        self.pending_dataowner_connections = []
        
        self.trusted_dataowner_connections = []
        
        self.auth_policy = None
        
        self.validation_data = self._clean_validation_data(validation_data_path)
        
        self.current_learner_index = 0
        
        self.model_path = "model.pt"
        
        self.part_trained_models = []

        torch.save(model, self.model_path)
        # The Researcher generates the model



        
    def _register_agent_listeners(self):
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.agent_controller.listen_webhooks())
        
        listeners=[{
            "handler": self._ml_messages_handler,
            "topic": "basicmessages"
        },
        {
            "handler": self._connection_handler,
            "topic": "connections"
        },
        {   "topic": "issue_credential",
            "handler": self._cred_handler
        },
        {
            "topic": "present_proof",
            "handler": self._proof_handler
        }]

        self.agent_controller.register_listeners(listeners, defaults=True)

    def _ml_messages_handler(self, payload):
        loop = asyncio.get_event_loop()
        connection_id =  payload["connection_id"]
        content = payload["content"]
        
        if connection_id in self.trusted_dataowner_connections:
            model_file = "part_trained_" + connection_id + ".pt"
            try:
                f = open(self.current_model_file, "wb+")
                byte_message = bytes.fromhex(content)
                f.write(byte_message)
                f.close()
            except Exception as e:
                print("Error writing file", e)
                return

            self.validate_model(model_file)
            
            part_trained = {
                "connection_id": connection_id,
                "model_file": model_file
            }
            
            self.part_trained_models.append(part_trained)
            
            if len(self.part_trained_models) == len(self.trusted_dataowner_connections):
                self.learning_complete.set_result(True)
            
        






        else:
            print("Expecting Message from the current learner hospital:", self.trusted_dataowner_connections[self.current_learner_index])
            print("Received message:", payload["content"], payload["connection_id"])




    def _connection_handler(self, payload):
        loop = asyncio.get_event_loop()
        print("Connection Handler Called")
        connection_id = payload["connection_id"]
        state = payload["state"]
        print(f"Connection {connection_id} in State {state}")
        for dataowner in self.pending_dataowner_connections:
            if dataowner["connection_id"] == connection_id:
                if state == "request":
                    print("Accepting request ", connection_id)
                    loop.run_until_complete(self.agent_controller.connections.accept_request(connection_id))
                if state == "response":
                    time.sleep(2)
                    print("Sending trust ping", connection_id)
                    loop.run_until_complete(self.agent_controller.messaging.trust_ping(connection_id, "hello"))

                if state == "active":

                    print("Pending dataowner connection moved to active. Challenging with auth policy if set")
                    if self.auth_policy:
                        loop = asyncio.get_event_loop()
                        proof_request_web_request = {
                            "connection_id": connection_id,
                            "proof_request": self.auth_policy,
                            "trace": False
                        }
                        response = loop.run_until_complete(self.agent_controller.proofs.send_request(proof_request_web_request))
                    else:
                        # No Auth Policy set
                        dataowner["is_trusted"].set_result(True)
                    break
                    
    def _cred_handler(self, payload):
        print("Handle Credentials")
        exchange_id = payload['credential_exchange_id']
        state = payload['state']
        role = payload['role']
        attributes = payload['credential_proposal_dict']['credential_proposal']['attributes']
        print(f"Credential exchange {exchange_id}, role: {role}, state: {state}")
        loop = asyncio.get_event_loop()

        if state == "offer_received":
            print(f"Offering: {attributes}")
            print("Requesting credential")
            loop.run_until_complete(self.agent_controller.issuer.send_request_for_record(exchange_id))
        elif state == "credential_received":
            print("Storing Credential")
            credential_id = "Research Authority " + exchange_id
            loop.run_until_complete(self.agent_controller.issuer.store_credential(exchange_id, credential_id))


        
    def _proof_handler(self, payload):
        print("Handle present proof")
        role = payload["role"]
        connection_id = payload["connection_id"]
        pres_ex_id = payload["presentation_exchange_id"]
        state = payload["state"]
        print(f"Role {role}, Exchange {pres_ex_id} in state {state}")
        loop = asyncio.get_event_loop()
        for dataowner in self.pending_dataowner_connections:
            if dataowner["connection_id"] == connection_id:
                if state == "request_received":
                    print("Received Authentication Challenge")

                    credentials_by_reft = {}
                    revealed = {}
                    self_attested = {}
                    predicates = {}

                    # select credentials to provide for the proof
                    credentials = loop.run_until_complete(self.agent_controller.proofs.get_presentation_credentials(pres_ex_id))
                    print("Credentials", credentials)

                    reveal_cred = credentials[0]
                    print("Revealed Credential")
                    if credentials:
                        for row in credentials:

                            for referent in row["presentation_referents"]:
                                if referent not in credentials_by_reft:
                                    credentials_by_reft[referent] = row

                    for referent in payload["presentation_request"]["requested_attributes"]:
                        if referent in credentials_by_reft:
                            revealed[referent] = {
                                "cred_id": credentials_by_reft[referent]["cred_info"][
                                    "referent"
                                ],
                                "revealed": True,
                            }



                    print("\nGenerate the proof")
                    proof = {
                        "requested_predicates": predicates,
                        "requested_attributes": revealed,
                        "self_attested_attributes": self_attested,
                    }
                    print(proof)
                    print("\nXXX")
                    print(predicates)
                    print(revealed)
                    print(self_attested)

                    loop.run_until_complete(self.agent_controller.proofs.send_presentation(pres_ex_id, proof))

                elif state == "presentation_received":

                    print("Verifying DataOwner Presentation")
                    verify = loop.run_until_complete(self.agent_controller.proofs.verify_presentation(pres_ex_id))
                    dataowner["is_trusted"].set_result(verify['state'] == "verified")
                    break
    

    def new_dataowner_invite(self):
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.agent_controller.connections.create_invitation())
        connection_id = response["connection_id"]
        invite_message = json.dumps(response['invitation'])

        print()
        print(
            "♫♫♫ > "

            + "STEP 1:"
            + " Send the aries invitation to the data owner"
        )
        print()
        print(invite_message)
        print()
        dataowner = {
            "connection_id": connection_id,
            "is_trusted": asyncio.Future()
        }
        self.pending_dataowner_connections.append(dataowner)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(dataowner["is_trusted"])
        
        if dataowner["is_trusted"].result():
            print("New Data Owner Connection Trusted: ", connection_id)
            self.trusted_dataowner_connections.append(connection_id)
        return
    
    def set_authentication_policy(self,proof_request):
        self.auth_policy = proof_request
        
    def _clean_validation_data(self, file_path):
        print("CLEANING THE VALIDATION SET")
        #Read in Data
        train_df = pd.read_csv(file_path)

#         print("VALIDATION DATA", train_df)

        ########## START DATA CLEANING ###############
        #Let’s get rid of the variables "Timestamp",“comments”, “state” just to make our lives easier.
        train_df = train_df.drop(['comments'], axis= 1)
        train_df = train_df.drop(['state'], axis= 1)
        train_df = train_df.drop(['Timestamp'], axis= 1)

        # Assign default values for each data type
        defaultInt = 0
        defaultString = 'NaN'
        defaultFloat = 0.0

        # Create lists by data tpe
        intFeatures = ['Age']
        stringFeatures = ['Gender', 'Country', 'self_employed', 'family_history', 'treatment', 'work_interfere',
                         'no_employees', 'remote_work', 'tech_company', 'anonymity', 'leave', 'mental_health_consequence',
                         'phys_health_consequence', 'coworkers', 'supervisor', 'mental_health_interview', 'phys_health_interview',
                         'mental_vs_physical', 'obs_consequence', 'benefits', 'care_options', 'wellness_program',
                         'seek_help']
        floatFeatures = []

        # Clean the NaN's
        for feature in train_df:
            if feature in intFeatures:
                train_df[feature] = train_df[feature].fillna(defaultInt)
            elif feature in stringFeatures:
                train_df[feature] = train_df[feature].fillna(defaultString)
            elif feature in floatFeatures:
                train_df[feature] = train_df[feature].fillna(defaultFloat)
            else:
                print('Error: Feature %s not recognized.' % feature)

        #clean 'Gender'
        #Slower case all columm's elements
        gender = train_df['Gender'].str.lower()
        #print(gender)

        #Select unique elements
        gender = train_df['Gender'].unique()

        #Made gender groups
        male_str = ["male", "m", "male-ish", "maile", "mal", "male (cis)", "make", "male ", "man","msle", "mail", "malr","cis man", "Cis Male", "cis male"]
        trans_str = ["trans-female", "something kinda male?", "queer/she/they", "non-binary","nah", "all", "enby", "fluid", "genderqueer", "androgyne", "agender", "male leaning androgynous", "guy (-ish) ^_^", "trans woman", "neuter", "female (trans)", "queer", "ostensibly male, unsure what that really means"]
        female_str = ["cis female", "f", "female", "woman",  "femake", "female ","cis-female/femme", "female (cis)", "femail"]

        for (row, col) in train_df.iterrows():

            if str.lower(col.Gender) in male_str:
                train_df['Gender'].replace(to_replace=col.Gender, value='male', inplace=True)

            if str.lower(col.Gender) in female_str:
                train_df['Gender'].replace(to_replace=col.Gender, value='female', inplace=True)

            if str.lower(col.Gender) in trans_str:
                train_df['Gender'].replace(to_replace=col.Gender, value='trans', inplace=True)

        #Get rid of bullshit
        stk_list = ['A little about you', 'p']
        train_df = train_df[~train_df['Gender'].isin(stk_list)]

        #complete missing age with mean
        train_df['Age'].fillna(train_df['Age'].median(), inplace = True)

        # Fill with media() values < 18 and > 120
        s = pd.Series(train_df['Age'])
        s[s<18] = train_df['Age'].median()
        train_df['Age'] = s
        s = pd.Series(train_df['Age'])
        s[s>120] = train_df['Age'].median()
        train_df['Age'] = s

        #Ranges of Age
        train_df['age_range'] = pd.cut(train_df['Age'], [0,20,30,65,100], labels=["0-20", "21-30", "31-65", "66-100"], include_lowest=True)

        #There are only 0.20% of self work_interfere so let's change NaN to "Don't know
        #Replace "NaN" string from defaultString

        train_df['work_interfere'] = train_df['work_interfere'].replace([defaultString], 'Don\'t know' )

        #Encoding data
        labelDict = {}
        for feature in train_df:
            le = preprocessing.LabelEncoder()
            le.fit(train_df[feature])
            le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
            train_df[feature] = le.transform(train_df[feature])
            # Get labels
            labelKey = 'label_' + feature
            labelValue = [*le_name_mapping]
            labelDict[labelKey] =labelValue

        #Get rid of 'Country'
        train_df = train_df.drop(['Country'], axis= 1)

        # Scaling Age
        scaler = MinMaxScaler()
        train_df['Age'] = scaler.fit_transform(train_df[['Age']])

        # define X and y
        feature_cols = ['Age', 'Gender', 'family_history', 'benefits', 'care_options', 'anonymity', 'leave', 'work_interfere']
        X = train_df[feature_cols]
        y = train_df.treatment

        # split X and y into training and testing sets
        X_test, y_test = X, y

        # Transform pandas dataframe to torch tensor for DL

        x_test_data = torch.from_numpy(X_test.values)
        x_test_data = x_test_data.float()
        

        y_test_data = []
        for data in y_test.values:
            y_test_data.append([data])
        y_test_data = torch.tensor(y_test_data).float()
        
        validation_data = {
            "x": x_test_data,
            "y": y_test_data,
        }
        

        print("VALIDATION SET HAS BEEN CLEANED")
        return validation_data

    
        
    def validate_model(self, model_file_path):


        model = torch.load(model_file_path)

        print("HOSPITAL MODEL LOADED")
        print("\nPRINTING PARAMETERS:\n\n")


        print(model)

        print('\n')

        for name, param in model.named_parameters():
            if param.requires_grad:
                print(name, param.data)

        # Validation Logic
        print("\n\n\nHOSPITAL IS VALIDATING")

        #BINARIZE PREDICTION FOR CONFUSION MATRIX

        pred = []

        for data in  model(self.validation_data["x"]):
            if data > .5:
                pred.append(1)
            else:
                pred.append(0)


        confusion = metrics.confusion_matrix(pred, self.validation_data["y"])

        print("Model loss on validation set: ", (model(self.validation_data["x"]) - self.validation_data["y"]).sum())
        print("Confusion Matrix:\n                Actual_True, Actual_False \n Predicted_True    ",confusion[1][1],"   |     ",confusion[1][0],"    \n Predicted_False   ",confusion[0][1],"     |      ",confusion[0][0],"    \n")
        
        
    def get_trusted_dataowner_connections(self):
        return self.trusted_dataowner_connections
    
    def initiate_learning(self):
        self.current_learner_index = 0

        f = open("model.pt", "rb")
        print("MODEL OPENED FOR TRANSPORT")

        contents = f.read()
        f.close()

        content = contents.hex()
        
        loop = asyncio.get_event_loop()

        print(f"Training model with {len(self.trusted_dataowner_connections)} DataOwners")
        
        self.learning_complete = asyncio.Future()
        for connection_id in self.trusted_dataowner_connections:

            loop.run_until_complete(self.agent_controller.messaging.send_message(connection_id, content))
        
        loop.run_until_complete(self.learning_complete)
        
        ## We need to aggregate the models 
        print(self.part_trained_models)
        
        print("LEARNING COMPLETE")
        
        
    
    

