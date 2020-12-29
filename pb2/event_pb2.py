# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: event.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='event.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\x0b\x65vent.proto\"G\n\x05\x65vent\x12\x15\n\x05sport\x18\x01 \x02(\x0e\x32\x06.sport\x12\x13\n\x0bmatch_title\x18\x02 \x02(\t\x12\x12\n\ndata_event\x18\x03 \x02(\t*a\n\x05sport\x12\x0c\n\x08\x42\x41SEBALL\x10\x01\x12\x0e\n\nBASKETBALL\x10\x02\x12\x0c\n\x08\x46OOTBALL\x10\x03\x12\n\n\x06\x42OXING\x10\x04\x12\x08\n\x04GOLF\x10\x05\x12\n\n\x06NASCAR\x10\x06\x12\n\n\x06TENNIS\x10\x07')
)

_SPORT = _descriptor.EnumDescriptor(
  name='sport',
  full_name='sport',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BASEBALL', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BASKETBALL', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FOOTBALL', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BOXING', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOLF', index=4, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NASCAR', index=5, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TENNIS', index=6, number=7,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=88,
  serialized_end=185,
)
_sym_db.RegisterEnumDescriptor(_SPORT)

sport = enum_type_wrapper.EnumTypeWrapper(_SPORT)
BASEBALL = 1
BASKETBALL = 2
FOOTBALL = 3
BOXING = 4
GOLF = 5
NASCAR = 6
TENNIS = 7



_EVENT = _descriptor.Descriptor(
  name='event',
  full_name='event',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sport', full_name='event.sport', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='match_title', full_name='event.match_title', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data_event', full_name='event.data_event', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=86,
)

_EVENT.fields_by_name['sport'].enum_type = _SPORT
DESCRIPTOR.message_types_by_name['event'] = _EVENT
DESCRIPTOR.enum_types_by_name['sport'] = _SPORT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

event = _reflection.GeneratedProtocolMessageType('event', (_message.Message,), dict(
  DESCRIPTOR = _EVENT,
  __module__ = 'event_pb2'
  # @@protoc_insertion_point(class_scope:event)
  ))
_sym_db.RegisterMessage(event)


# @@protoc_insertion_point(module_scope)
