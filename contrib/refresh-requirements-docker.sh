#!/bin/sh -e
#
# Script to refresh requirement files using a Docker container
#
# Copyright (C) 2022-2023 Libre Space Foundation <https://libre.space/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

DOCKER_IMAGE="debian:bullseye"

REQUIREMENTS="docker"

# Check for required utilities
for req in $REQUIREMENTS; do
	if ! which "$req" >/dev/null; then
		if [ -z "$has_missing" ]; then
			echo "$(basename "$0"): Missing script requirements!" 1>&2
			echo "Please install:" 1>&2
			has_missing=1
		fi
		echo " - '$req'" 1>&2
	fi
done
if [ -n "$has_missing" ]; then
	exit 1
fi

{
	cat << EOF
command -v apt-get >/dev/null && {
apt-get -y update
apt-get -qy install virtualenv git
[ -f /projectdir/packages.debian ] && xargs -r -a /projectdir/packages.debian apt-get -qy install
}
EOF
	cat << EOF
command -v apk >/dev/null && {
apk add -qU py3-virtualenv git
[ -f /projectdir/packages.alpine ] && xargs -r -a /projectdir/packages.alpine apk add -qU
}
EOF
	cat << EOF
umask $(umask)
cd /projectdir
EOF
	cat "$(dirname "$0")/refresh-requirements.sh"
	cat << EOF
chown "$(id -u):$(id -g)" constraints.txt requirements.txt
[ -f requirements-dev.txt ] && chown "$(id -u):$(id -g)" requirements-dev.txt
EOF
} | docker run -i --rm -v "$(pwd):/projectdir" "$DOCKER_IMAGE" /bin/sh -e -s
