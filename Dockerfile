# SatNOGS Client image
#
# Copyright (C) 2022 Libre Space Foundation <https://libre.space/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

ARG GNURADIO_IMAGE_TAG=3.8.2.0
FROM librespace/gnuradio:${GNURADIO_IMAGE_TAG}
LABEL org.opencontainers.image.authors='SatNOGS project <dev@satnogs.org>'

ARG SATNOGS_CLIENT_UID=999
ARG SATNOGS_CLIENT_VARSTATEDIR=/var/lib/satnogs-client

# Add unprivileged system user
RUN groupadd -r -g ${SATNOGS_CLIENT_UID} satnogs-client \
	&& useradd -r -u ${SATNOGS_CLIENT_UID} \
		-g satnogs-client \
		-d ${SATNOGS_CLIENT_VARSTATEDIR} \
		-s /bin/false \
		-G audio,dialout,plugdev \
		satnogs-client

# Create application varstate directory
RUN install -d -o ${SATNOGS_CLIENT_UID} -g ${SATNOGS_CLIENT_UID} ${SATNOGS_CLIENT_VARSTATEDIR}

# Copy source code
COPY . /usr/local/src/satnogs-client/

# Install system packages
RUN apt-get update \
	&& xargs -a /usr/local/src/satnogs-client/packages.debian apt-get install -qy python3-pip \
	&& rm -r /var/lib/apt/lists/*

# Install Python dependencies and application
RUN echo "[global]" > /etc/pip.conf \
	&& echo "extra-index-url=https://www.piwheels.org/simple" >> /etc/pip.conf \
	&& pip install --no-cache-dir --no-deps \
		-r /usr/local/src/satnogs-client/requirements.txt \
		/usr/local/src/satnogs-client
