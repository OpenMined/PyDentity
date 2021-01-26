import asyncio
from aries_basic_controller.aries_controller import AriesAgentController
import json

import torch
import traceback

# models
from torch import nn
from torch import optim
from torch.autograd import Variable
import os
import sys
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import torch

# prep
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.datasets import make_classification
from sklearn.preprocessing import binarize, LabelEncoder, MinMaxScaler



class Hospital:

    def __init__(self, agent_config, data_location):

        self.agent_controller = AriesAgentController(webhook_host=agent_config["webhook_host"],webhook_port=agent_config["webhook_port"],                                       webhook_base=agent_config["webhook_base"], admin_url=agent_config["admin_url"])

        self._register_agent_listeners()

        self.pending_connections = []

        self.trusted_connection_ids = []

        self.auth_policy = None

        self.data = self._process_data(data_location)


    def _register_agent_listeners(self):

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.agent_controller.listen_webhooks())

        listeners = [{
                "handler": self._ml_messages_handler,
                "topic": "basicmessages"
            },
            {
                "handler": self._connection_handler,
                "topic": "connections"
            },
            {"topic": "issue_credential",
             "handler": self._cred_handler
             },
            {
                "topic": "present_proof",
                "handler": self._proof_handler
            }]

        self.agent_controller.register_listeners(listeners, defaults=True)

    def _ml_messages_handler(self, payload):

        connection_id = payload["connection_id"]
        print(f"ML Message from {connection_id}")

        if connection_id in self.trusted_connection_ids:
            print("Open file")
            try:
                f = open("untrained_model.pt", "wb+")
                # self.log(bytes.fromhex(message["content"]))
                byte_message = bytes.fromhex(payload["content"])
                f.write(byte_message)
                f.close()

            except Exception as e:
                print("Error writing file", e)
                return

            print("learning")

            self.hospital_learn()
            print("Learnt ")

            trained_model = None
            try:
                trained_file = open("trained_model.pt", "rb")
                print("Trained file open")
                trained_model = trained_file.read()
                trained_file.close()
            except:
                print("Unable to open trained model")


            print("connection ID", connection_id)
            if trained_model:
                content = trained_model.hex()
                asyncio.get_event_loop().create_task(self.agent_controller.messaging.send_message(connection_id, content))
        else:
            print(f"Do not trust this connection to send ml messages {connection_id}")
            print("MEssage : ", payload["content"])


    def _connection_handler(self, payload):
        loop = asyncio.get_event_loop()
        print("Connection Handler Called")
        connection_id = payload["connection_id"]
        state = payload["state"]
        print(f"Connection {connection_id} in State {state}")
        for connection in self.pending_connections:
            if connection["connection_id"] == connection_id:
                if state == "active":

                    print("Pending connection moved to active. Challenging with auth policy if set")
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
                        print("No Auth Policy set")
                        connection["is_trusted"].set_result(True)
                    break


    def _cred_handler(self, payload):
        print("Handle Credentials")
        exchange_id = payload['credential_exchange_id']
        state = payload['state']
        role = payload['role']
        attributes = payload['credential_proposal_dict']['credential_proposal']['attributes']
        print(f"Credential exchange {exchange_id}, role: {role}, state: {state}")
        print(f"Offering: {attributes}")

    def _proof_handler(self, payload):
        print("Handle present proof")
        role = payload["role"]
        connection_id = payload["connection_id"]
        pres_ex_id = payload["presentation_exchange_id"]
        state = payload["state"]
        print(f"Role {role}, Exchange {pres_ex_id} in state {state}")

        if state == "presentation_received":
            for connection in self.pending_dataowner_connections:
                if connection["connection_id"] == connection_id:
                    loop = asyncio.get_event_loop()

                    print("Verifying DataOwner Presentation")
                    verify = loop.run_until_complete(self.agent_controller.proofs.verify_presentation(pres_ex_id))
                    connection["is_trusted"].set_result(verify['state'] == "verified")
                    break

    def _process_data(self, file_path):
        # Read in Data
        train_df = pd.read_csv(file_path)

        ########## START DATA CLEANING ###############

        # dealing with missing data
        # Let’s get rid of the variables "Timestamp",“comments”, “state” just to make our lives easier.
        train_df = train_df.drop(['comments'], axis=1)
        train_df = train_df.drop(['state'], axis=1)
        train_df = train_df.drop(['Timestamp'], axis=1)

        # Assign default values for each data type
        defaultInt = 0
        defaultString = 'NaN'
        defaultFloat = 0.0

        # Create lists by data tpe
        intFeatures = ['Age']
        stringFeatures = ['Gender', 'Country', 'self_employed', 'family_history', 'treatment', 'work_interfere',
                          'no_employees', 'remote_work', 'tech_company', 'anonymity', 'leave',
                          'mental_health_consequence',
                          'phys_health_consequence', 'coworkers', 'supervisor', 'mental_health_interview',
                          'phys_health_interview',
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

        # clean 'Gender'
        # Slower case all columm's elements
        gender = train_df['Gender'].str.lower()
        # print(gender)

        # Select unique elements
        gender = train_df['Gender'].unique()

        # Made gender groups
        male_str = ["male", "m", "male-ish", "maile", "mal", "male (cis)", "make", "male ", "man", "msle", "mail",
                    "malr", "cis man", "Cis Male", "cis male"]
        trans_str = ["trans-female", "something kinda male?", "queer/she/they", "non-binary", "nah", "all", "enby",
                     "fluid", "genderqueer", "androgyne", "agender", "male leaning androgynous", "guy (-ish) ^_^",
                     "trans woman", "neuter", "female (trans)", "queer",
                     "ostensibly male, unsure what that really means"]
        female_str = ["cis female", "f", "female", "woman", "femake", "female ", "cis-female/femme", "female (cis)",
                      "femail"]

        for (row, col) in train_df.iterrows():

            if str.lower(col.Gender) in male_str:
                train_df['Gender'].replace(to_replace=col.Gender, value='male', inplace=True)

            if str.lower(col.Gender) in female_str:
                train_df['Gender'].replace(to_replace=col.Gender, value='female', inplace=True)

            if str.lower(col.Gender) in trans_str:
                train_df['Gender'].replace(to_replace=col.Gender, value='trans', inplace=True)

        # Get rid of bullshit
        stk_list = ['A little about you', 'p']
        train_df = train_df[~train_df['Gender'].isin(stk_list)]

        # complete missing age with mean
        train_df['Age'].fillna(train_df['Age'].median(), inplace=True)

        # Fill with media() values < 18 and > 120
        s = pd.Series(train_df['Age'])
        s[s < 18] = train_df['Age'].median()
        train_df['Age'] = s
        s = pd.Series(train_df['Age'])
        s[s > 120] = train_df['Age'].median()
        train_df['Age'] = s

        # Ranges of Age
        train_df['age_range'] = pd.cut(train_df['Age'], [0, 20, 30, 65, 100],
                                       labels=["0-20", "21-30", "31-65", "66-100"], include_lowest=True)

        # There are only 0.20% of self work_interfere so let's change NaN to "Don't know
        # Replace "NaN" string from defaultString

        train_df['work_interfere'] = train_df['work_interfere'].replace([defaultString], 'Don\'t know')

        # Encoding data
        labelDict = {}
        for feature in train_df:
            le = preprocessing.LabelEncoder()
            le.fit(train_df[feature])
            le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
            train_df[feature] = le.transform(train_df[feature])
            # Get labels
            labelKey = 'label_' + feature
            labelValue = [*le_name_mapping]
            labelDict[labelKey] = labelValue

        # Get rid of 'Country'
        train_df = train_df.drop(['Country'], axis=1)

        # Scaling Age
        scaler = MinMaxScaler()
        train_df['Age'] = scaler.fit_transform(train_df[['Age']])

        # define X and y
        feature_cols = ['Age', 'Gender', 'family_history', 'benefits', 'care_options', 'anonymity', 'leave',
                        'work_interfere']
        X = train_df[feature_cols]
        y = train_df.treatment

        # split X and y into training and testing sets
        X_train, y_train = X, y

        # Transform pandas dataframe to torch tensor for DL

        x_train_data = torch.from_numpy(X_train.values)
        x_train_data = x_train_data.float()

        y_train_data = []
        for data in y_train.values:
            y_train_data.append([data])
        y_train_data = torch.tensor(y_train_data).float()
        
        print("Data Processed")
        
        return {
            "x": x_train_data,
            "y": y_train_data
        }

    def hospital_learn(self):

        model_dir = "untrained_model.pt"

        print(model_dir)

        # Pull in model
        try:
            model = torch.load(model_dir)
        except Exception as e:
            print("HOSPITAL FAILED TO LOAD MODEL")
            print("Exception Value: ", e)
            print("Traceback ", traceback.format_exc())
        #     return False

        print("HOSPITAL MODEL LOADED")

        # Training Logic
        print("HOSPITAL IS TRAINING")

        # Define Optimizer
        opt = optim.SGD(params=model.parameters(), lr=0.1)

        # opt = torch.optim.SGD(model.parameters(), lr=0.05)

        # Apply Differential Privacy

        # privacy_engine = PrivacyEngine(model, batch_size=333, sample_size=1000, alphas=[10, 100],
        #                            noise_multiplier=1.3, max_grad_norm=1.0)

        # privacy_engine.attach(opt)

        for iter in range(50000):

            # 1) erase previous gradients (if they exist)
            opt.zero_grad()
            # log_msg("TRAIN DATA", x_train_data)

            # 2) make a prediction
            pred = model(self.data["x"])

            # 3) calculate how much we missed
            loss = (((self.data["y"] - pred) ** 2).sum()) / len(self.data["x"])

            # 4) figure out which weights caused us to miss
            loss.backward()

            # 5) change those weights
            opt.step()

            # 6) log_msg our progress
            if (iter % 5000 == 0):
                print("loss at epoch ", iter, ": ", loss.data)

        torch.save(model, "trained_model.pt")

    def set_authentication_policy(self, proof_request):
        self.auth_policy = proof_request

    def establish_research_connection(self, invitation):

        loop = asyncio.get_event_loop()

        response = loop.run_until_complete(self.agent_controller.connections.accept_connection(invitation))

        connection_id = response["connection_id"]

        pending_connection = {
            "connection_id": connection_id,
            "is_trusted": asyncio.Future()
        }

        self.pending_connections.append(pending_connection)
        print("Establishing connection")
        loop.run_until_complete(pending_connection["is_trusted"])

        if pending_connection["is_trusted"].result():
            self.trusted_connection_ids.append(connection_id)

            print(f"Trusted Research Connection Established - {connection_id}")