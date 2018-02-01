.DEFAULT_GOAL := all

.PHONY: pip_install
pip_install:
	@for d in $$( find . -name lbr.yaml | xargs dirname ); do \
	  if [ -e $$d/requirements.txt ]; then \
	    pip install -U -r $$d/requirements.txt -t $$d; \
	  fi; \
	done

%:
	cfn-lbr-registry $@