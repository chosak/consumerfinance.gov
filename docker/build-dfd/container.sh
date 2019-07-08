#!/usr/bin/env bash

# Fail when any command fails.
set -e

artifact_name=cfgov
artifact_label=current
artifact_release=build

build_artifact="${artifact_name}_${artifact_label}.zip"
release_artifact="${artifact_name}_${artifact_label}_${artifact_release}.zip"
cfgov_refresh_volume=/cfgov
webfonts_path="$cfgov_refresh_volume/static.in/cfgov-fonts"

# Verify that source volume has been mapped.
if [ ! -d "$cfgov_refresh_volume" ]; then
    echo "Source directory $cfgov_refresh_volume does not exist."
    echo "Did you forget to mount the Docker volume?"
    exit 1
fi

# Install build requirements.
yum install -y centos-release-scl
yum install -y gcc git python27

source /opt/rh/python27/enable

pip install -U pip
pip install -U git+https://github.com/cfpb/drama-free-django.git

curl -sL https://rpm.nodesource.com/setup_10.x | bash -
curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo
yum install -y nodejs yarn

# Run the frontend build.
pushd "$cfgov_refresh_volume"
./frontend.sh production
popd

# drama-free-django build step.
build_args=(
    "$cfgov_refresh_volume/cfgov"
    "$artifact_name"
    "$artifact_label"
    -f
    -r "$cfgov_refresh_volume/requirements/optional-public.txt"
    -r "$cfgov_refresh_volume/requirements/deployment.txt"
)


if [ -d "$webfonts_path" ]; then
    build_args+=("--static" "$webfonts_path")
fi

no-drama build "${build_args[@]}"

# drama-free-django release step.

# This is just a placeholder that gets replaced by Ansible.
echo "{}" > ./dfd_env.json

# This is used by DFD to set Django's settings.STATIC_ROOT.
echo '{"static_out": "../../../static"}' > ./dfd_paths.json

no-drama release \
    "./$build_artifact" \
    ./dfd_env.json \
    "$artifact_release" \
    --paths ./dfd_paths.json

# Copy release artifact to source directory.
cp "$release_artifact" "$cfgov_refresh_volume"
echo "Generated $release_artifact in $cfgov_refresh_volume."
