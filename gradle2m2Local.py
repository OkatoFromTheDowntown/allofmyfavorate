#!/usr/bin/python

import sys
import os
import subprocess
import glob
import shutil

# same to ./gradlew publishToMavenLocal
def maven2Local(argv):
    project_dir = os.path.dirname(os.path.realpath(__file__))
    repo_dir = os.path.join(project_dir, "android-tooling-repo")
    temp_home = os.path.join(project_dir, ".gradle_home")
    if not os.path.isdir(temp_home):
        os.makedirs(temp_home)
    
    if os.path.isdir(repo_dir):
        shutil.rmtree(repo_dir)
    
    subprocess.call(["gradle", "-g", temp_home, "-Dbuild.network_access=allow"])
    
    cache_files = os.path.join(temp_home, "caches/modules-*/files-*")
    for cache_dir in glob.glob(cache_files):
        for cache_group_id in os.listdir(cache_dir):
            cache_group_dir = os.path.join(cache_dir, cache_group_id)
            repo_group_dir = os.path.join(repo_dir, cache_group_id.replace('.', '/'))
            for cache_artifact_id in os.listdir(cache_group_dir):
                cache_artifact_dir = os.path.join(cache_group_dir, cache_artifact_id)
                repo_artifact_dir = os.path.join(repo_group_dir, cache_artifact_id)
                for cache_version_id in os.listdir(cache_artifact_dir):
                    cache_version_dir = os.path.join(cache_artifact_dir, cache_version_id)
                    repo_version_dir = os.path.join(repo_artifact_dir, cache_version_id)
                    if not os.path.isdir(repo_version_dir):
                        os.makedirs(repo_version_dir)
                    cache_items = os.path.join(cache_version_dir, "*/*")
                    for cache_item in glob.glob(cache_items):
                        cache_item_name = os.path.basename(cache_item)
                        repo_item_path = os.path.join(repo_version_dir, cache_item_name)
                        print "%s:%s:%s (%s)" % (cache_group_id, cache_artifact_id, cache_version_id, cache_item_name)
                        shutil.copyfile(cache_item, repo_item_path)
    shutil.rmtree(temp_home)
    return 0

if __name__ == "__main__":
    sys.exit(maven2Local(sys.argv))
