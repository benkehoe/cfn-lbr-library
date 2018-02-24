#Copyright 2018 iRobot Corporation
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

.DEFAULT_GOAL := all

CFN_CUSTOM_RESOUCE_CACHE_FILE = .cfn_custom_resource

.PHONY: build
build:
	@for d in $$( find . -name lbr.yaml | xargs dirname ); do \
	  if [ -e $$d/requirements.txt ]; then \
	    pip install -U -r $$d/requirements.txt -t $$d; \
	  fi; \
	  if [ -e $$d/requires-cfn-custom-resource ]; then \
	    if [ -n .cfn_custom_resource.py ]; then \
	      wget -O $(CFN_CUSTOM_RESOUCE_CACHE_FILE) https://raw.githubusercontent.com/iRobotCorporation/cfn-custom-resource/master/cfn_custom_resource/cfn_custom_resource.py \
	    fi; \
	    cp $(CFN_CUSTOM_RESOUCE_CACHE_FILE) $$d/cfn_custom_resource.py \
	  fi; \
	done

%:
	cfn-lbr-registry $@