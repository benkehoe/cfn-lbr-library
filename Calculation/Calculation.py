"""
MyCalculation:
  Type: Custom::Calculation
  Properties:
    Fraction: 0-1
    -OR-
    Percent: 0-100

Ref is percent as a string
Attributes are Fraction and Percent

Copyright 2018 iRobot Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import division

from cfn_custom_resource import CloudFormationCustomResource

class Calculation(CloudFormationCustomResource):
    DISABLE_PHYSICAL_RESOURCE_ID_GENERATION = True
    
    def _convert_fraction(self):
        if 'Fraction' in self.resource_properties:
            fraction = float(self.resource_properties['Fraction'])
            percent = int(fraction * 100)
        else:
            percent = int(self.resource_properties['Percent'])
            fraction = float(percent) / 100
        
        self.physical_resource_id = str(percent)
        return {
            'Fraction': fraction,
            'Percent': percent,
        }
    
    def _evaluate(self):
        if any(k in self.resource_properties for k in ['Fraction', 'Percent']):
            return self._convert_fraction()
        
        raise ValueError('Invalid properties')
    
    def create(self):
        return self._evaluate()
    
    def update(self):
        return self._evaluate()
    
    def delete(self):
        pass