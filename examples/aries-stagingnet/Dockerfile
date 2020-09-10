FROM bcgovimages/von-image:py36-1.14-0
#FROM bcgovimages/aries-cloudagent:py36-1.14-1_0.5.1

USER root
RUN apt-get update
RUN apt-get update && apt-get install -y gcc
#RUN apt-get install -y wget gcc openssl pkg-config libssl-dev
## Rust
#ENV RUSTUP_HOME=/usr/local/rustup \
#    CARGO_HOME=/usr/local/cargo \
#    PATH=/usr/local/cargo/bin:$PATH \
#    RUST_VERSION=1.41.1
#
#RUN set -eux; \
#    dpkgArch="$(dpkg --print-architecture)"; \
#    case "${dpkgArch##*-}" in \
#        amd64) rustArch='x86_64-unknown-linux-gnu'; rustupSha256='ad1f8b5199b3b9e231472ed7aa08d2e5d1d539198a15c5b1e53c746aad81d27b' ;; \
#        armhf) rustArch='armv7-unknown-linux-gnueabihf'; rustupSha256='6c6c3789dabf12171c7f500e06d21d8004b5318a5083df8b0b02c0e5ef1d017b' ;; \
#        arm64) rustArch='aarch64-unknown-linux-gnu'; rustupSha256='26942c80234bac34b3c1352abbd9187d3e23b43dae3cf56a9f9c1ea8ee53076d' ;; \
#        i386) rustArch='i686-unknown-linux-gnu'; rustupSha256='27ae12bc294a34e566579deba3e066245d09b8871dc021ef45fc715dced05297' ;; \
#        *) echo >&2 "unsupported architecture: ${dpkgArch}"; exit 1 ;; \
#    esac; \
#    url="https://static.rust-lang.org/rustup/archive/1.21.1/${rustArch}/rustup-init"; \
#    wget "$url"; \
#    echo "${rustupSha256} *rustup-init" | sha256sum -c -; \
#    chmod +x rustup-init; \
#    ./rustup-init -y --no-modify-path --profile minimal --default-toolchain $RUST_VERSION; \
#    rm rustup-init; \
#    chmod -R a+w $RUSTUP_HOME $CARGO_HOME; \
#    rustup --version; \
#    cargo --version; \
#    rustc --version;
#
#
#ADD https://github.com/sovrin-foundation/libsovtoken/archive/v1.0.1.tar.gz libsovtoken.tar.gz
#ENV LIBINDY_DIR=/home/indy/.local/lib
#ENV LD_LIBRARY_PATH=/home/indy/.local/lib
#RUN tar xzvf libsovtoken.tar.gz; \
#        cd libsovtoken-1.0.1/libsovtoken; \
#        cargo build
#ENV LIBSOVTOKEN=/home/indy/libsovtoken-1.0.1/libsovtoken/target/debug/libsovtoken.so
#ADD . .

#RUN pip3 install --no-cache-dir -e .
RUN pip3 install aries-cloudagent

ADD https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 ./jq
RUN chmod +x ./jq
COPY startup.sh startup.sh
RUN chmod +x ./startup.sh
COPY ngrok-wait.sh wait.sh
RUN chmod +x ./wait.sh

USER $user

CMD ./wait.sh ./startup.sh