# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: banks.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'banks.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x62\x61nks.proto\x12\x04\x62\x61nk\"U\n\x0e\x44\x65positRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\x05\x12\x10\n\x08\x65vent_id\x18\x02 \x01(\x05\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x05\x12\x0c\n\x04\x64\x65st\x18\x04 \x01(\x05\"3\n\x0f\x44\x65positResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07\x62\x61lance\x18\x02 \x01(\x05\"V\n\x0fWithdrawRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\x05\x12\x10\n\x08\x65vent_id\x18\x02 \x01(\x05\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x05\x12\x0c\n\x04\x64\x65st\x18\x04 \x01(\x05\"4\n\x10WithdrawResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07\x62\x61lance\x18\x02 \x01(\x05\"C\n\x0cQueryRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\x05\x12\x10\n\x08\x65vent_id\x18\x02 \x01(\x05\x12\x0c\n\x04\x64\x65st\x18\x03 \x01(\x05\" \n\rQueryResponse\x12\x0f\n\x07\x62\x61lance\x18\x01 \x01(\x05\"9\n\rUpdateRequest\x12\x10\n\x08\x65vent_id\x18\x01 \x01(\x05\x12\x16\n\x0e\x62\x61lance_change\x18\x02 \x01(\x05\"!\n\x0eUpdateResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xe7\x01\n\x04\x42\x61nk\x12\x36\n\x07\x44\x65posit\x12\x14.bank.DepositRequest\x1a\x15.bank.DepositResponse\x12\x39\n\x08Withdraw\x12\x15.bank.WithdrawRequest\x1a\x16.bank.WithdrawResponse\x12\x30\n\x05Query\x12\x12.bank.QueryRequest\x1a\x13.bank.QueryResponse\x12:\n\rReceiveUpdate\x12\x13.bank.UpdateRequest\x1a\x14.bank.UpdateResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'banks_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DEPOSITREQUEST']._serialized_start=21
  _globals['_DEPOSITREQUEST']._serialized_end=106
  _globals['_DEPOSITRESPONSE']._serialized_start=108
  _globals['_DEPOSITRESPONSE']._serialized_end=159
  _globals['_WITHDRAWREQUEST']._serialized_start=161
  _globals['_WITHDRAWREQUEST']._serialized_end=247
  _globals['_WITHDRAWRESPONSE']._serialized_start=249
  _globals['_WITHDRAWRESPONSE']._serialized_end=301
  _globals['_QUERYREQUEST']._serialized_start=303
  _globals['_QUERYREQUEST']._serialized_end=370
  _globals['_QUERYRESPONSE']._serialized_start=372
  _globals['_QUERYRESPONSE']._serialized_end=404
  _globals['_UPDATEREQUEST']._serialized_start=406
  _globals['_UPDATEREQUEST']._serialized_end=463
  _globals['_UPDATERESPONSE']._serialized_start=465
  _globals['_UPDATERESPONSE']._serialized_end=498
  _globals['_BANK']._serialized_start=501
  _globals['_BANK']._serialized_end=732
# @@protoc_insertion_point(module_scope)