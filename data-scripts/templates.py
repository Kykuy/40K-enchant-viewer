#!/usr/bin/env python3

# A set of Javascript templates, for use with Python's str.format()

################################################################################

DATA_TEMPLATE='''
var __version__ = "{version}";

var SLOTS = [
{slots}
];

var RECT_SLOTS = [
  "main_implant",
  "body",
  "inoculator",
  "weapon",
  "offhand",
];

// Object constructor
function Enchant(name, str, items, slots, quality, doubled, groups, range) {{
  this.name = name;
  this.str = str.includes('Focus/Adrenaline/Data-flux') ? str.replace('Focus/Adrenaline/Data-flux', 'Focus/Adrenaline/Warp Heat/Data-flux') : str;
  this.items = items;
  this.slots = slots;
  this.quality = quality;
  this.doubled = doubled;
  this.groups = groups;
  this.range = range;
}}

var enchants = [
{enchants}
];

var slot_items = new Map([
{item_types}
]);

'''

# for cleaning untagged s1 enchants, add after enchants variable declaration
# (not needed anymore, I moved this part to gen_data_js.py run) - Kykuy
# // untagged s1 enchants cleanup
# enchants = enchants.filter( (enchant) => !enchant.str.toLowerCase().includes('inferno') );

################################################################################

ENCHANT_TEMPLATE='''new Enchant('{name}',
              "{desc}",
              [{items}],
              [{slots}],
              '{quality}',
              {doubled},
              [{groups}]),
'''
