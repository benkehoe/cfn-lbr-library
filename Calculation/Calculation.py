"""
MyCalculation:
  Type: Custom::Calculation
  Properties:
    Fraction: 0-1
    -OR-
    Percent: 0-100

Ref is percent as a string
Attributes are Fraction and Percent
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