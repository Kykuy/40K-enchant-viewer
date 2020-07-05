#!/usr/bin/env python3

from enum import Enum
from fsm import FSM

# Exclude psalms, etc.
VALID_QUALITY=['primary','secondary','relic','morality']

class Enchant():
  def __init__(self, name):
    self.name = name # str
    self.desc = None # str
    self.desc_repl = None # str
    self.shortcuts = [] # [str, ...]
    self.slots = [] # [str, ...]
    self.items = [] # [str, ...]
    self.quality = None # str
    self.groups = [] # [str, ...]
    self.range = None # (low, high)

  def __str__(self):
    s = '<Enchant '+self.name+' '+str((self.desc,self.desc_repl,self.shortcuts,self.quality,self.groups,self.range))+'>'
    return s

_S = Enum('_S', 'TOP ITEMS ENCHANT, VALUES')

# Complex FSM actions 
def capture_item(M,D):
  D['shortcuts'][M[0]] = M[1].split(',')

def create_enchant(M,D):
  D['temp'] = Enchant(M[0])

def translate_quality(M,D):
  qual = M[0]
  T = { 'godlike':'relic' }
  if qual in T:
    qual = T[qual]
  D['temp'].quality = qual

def commit_enchant(M,D):
  if D['temp'].quality in VALID_QUALITY:
    D['enchants'].append(D['temp'])
  return _S.TOP

def set_range(M,D):
  D['temp'].range = float(M[0]), float(M[1])

def set_shortcuts(M,D):
  if M[0]=='':
    D['temp'].shortcuts = []
  else:
    D['temp'].shortcuts = M[0].split(',')

machine = {
  _S.TOP: [
    (r'Templates', lambda: _S.ITEMS),
    (r'Enchantment', lambda: _S.ENCHANT),
    (r'', None),
  ],
  _S.ITEMS: [
    (r'{', None),
    (r'(.*)=(.*)', capture_item),
    (r'}', lambda: _S.TOP),
  ],
  _S.ENCHANT: [
    (r'{', None),
    (r'Name=(.*)', create_enchant),
    (r'NameID=(.*)', lambda M,D: setattr(D['temp'],'desc',str.lower(M[0]))),
    (r'Property=(.*)', lambda M,D: setattr(D['temp'],'desc_repl',M[0])),
    (r'ArtifactTypes=(.*)', set_shortcuts),
    (r'EnchantQuality=(.*)', translate_quality),
    (r'Groups=(.*)', lambda M,D: setattr(D['temp'],'groups',M[0].split(','))),
    (r'Values$', lambda: _S.VALUES),
    (r'}', commit_enchant),
    (r'.*', None),
  ],
  _S.VALUES: [
    (r'100=(.*),(.*)', set_range),
    (r'(.*)=(.*),(.*)',None), # FIXME: item level interpolation is NYI (@100)
    (r'}', lambda: _S.ENCHANT),
    (r'.*', None),
  ]
}
  
def parse_enchants(file):
  fsm = FSM(_S, _S.TOP, [_S.TOP], machine)
  fsm.reset()
  fsm.data = {'shortcuts':{}, 'enchants':[], 'temp': None}
  #fsm.tracing(True)

  data = fsm.parse(file)

  return data['shortcuts'], data['enchants']

if __name__=='__main__':
  with open('enchantments.cfg') as f:
    shortcuts,enchants = parse_enchants(f)
    print(str(len(shortcuts))+' shortcuts')
    print(str(len(enchants))+' enchants')
