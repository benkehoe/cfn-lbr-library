.DEFAULT_GOAL := all

.PHONY: build
build:
	@for d in $$( find . -name lbr.yaml | xargs dirname ); do \
	  if [ -e $$d/requirements.txt ]; then \
	    pip install -U -r $$d/requirements.txt -t $$d; \
	  fi; \
	  if [ -e $$d/requires-cfn-custom-resource ] && [ -n $$d/cfn_custom_resource.py ]; then \
	    (cd $$d && wget https://github.com/iRobotCorporation/cfn-custom-resource/blob/master/cfn_custom_resource/cfn_custom_resource.py) \
	  fi; \
	done

%:
	cfn-lbr-registry $@