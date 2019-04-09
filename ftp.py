import ftplib
from ftplib import FTP
import logging
import os
import argparse
import json

DEBUG_LOG_LEVEL = 2

class FTPClient:
  def __init__(self, debug_level=DEBUG_LOG_LEVEL):
    self.ftp = 0
    self.debug_level = debug_level
    self.host = ''

  def connect(self, addr, username, password):
    self.host, self.port = addr
    self.ftp = FTP()
    self.ftp.set_debuglevel(self.debug_level)
    try:
      logging.debug('Connecting %s:%s'%(self.host, self.port))
      self.ftp.connect(self.host, self.port)
    except OSError as err:
      logging.error("Connect %s:%d failed!, %s"%(self.host, self.port, err))
      return False
    try:
      self.ftp.login(username, password)
    except ftplib.all_errors as err:
      logging.error("Login %s failed!, %s"%(username, err))
      return False

    logging.info('Connect %s:%d success'%addr)
    return True

  def download(self, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath,'wb')
    try:
      self.ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
      logging.info('Download %s from %s success'%(remotepath, self.host))
    except ftplib.all_errors as err:
      logging.error("Download %s from %s failed!, %s"%(remotepath, self.host, err))
    fp.close()

  def upload(self, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    try:
      self.ftp.storbinary('STOR '+ remotepath , fp, bufsize)
      logging.info('Upload %s from %s success'%(remotepath, self.host))
    except ftplib.all_errors as err:
      logging.error("Upload %s from %s failed!, %s"%(localpath, self.host, err))
    fp.close()

  def delete(self, remotepath):
    try:
      self.ftp.delete(remotepath)
      logging.info('Upload %s from %s success'%(remotepath, self.host))
    except ftplib.all_errors as err:
      logging.error("Delete %s from %s failed!, %s"%(remotepath, self.host, err))
  

def loadFTPServerList(config_file):
  server_list = []
  with open(config_file) as config:
    config_dict = json.load(config)
    logging.debug(config_dict)
    ftp_servers = config_dict['ftp_server']
    for server in ftp_servers:
      server_list.append((server["ip"], server["port"]))

  return server_list


if __name__ == "__main__":
  LOG_FORMAT = "[%(asctime)s:%(levelname)s:%(funcName)s]  %(message)s"
  log_level = logging.DEBUG
  logging.basicConfig(level=log_level, format=LOG_FORMAT)

  arg_parser = argparse.ArgumentParser(description='manual to this script')
  arg_parser.add_argument('-c', '--config_file', help='config file', type=str)
  arg_parser.add_argument('-d', '--delete', help='delete file', type=str)
  arg_parser.add_argument('-u', '--upload', help='upload file', action="store_true")
  arg_parser.add_argument('-p', '--pull', help='pull file', action="store_true")
  arg_parser.add_argument('-r', '--remote_path', help='remote path', type=str)
  arg_parser.add_argument('-l', '--local_path', help='local path', type=str)
  args = arg_parser.parse_args()

  config_file = args.config_file

  ftp_list = loadFTPServerList(config_file)
  logging.debug(ftp_list)

  ftp_client_list = []
  for ftp_host in ftp_list:
    ftp_client = FTPClient(0)
    ret = ftp_client.connect(ftp_host,
                     'qpy3', 'qpy3')

    if ret:
      ftp_client_list.append(ftp_client)

  
  if args.delete:
    delete_path = args.delete
    for client in ftp_client_list:
      client.delete(delete_path)
  elif args.upload:
    remote_path = args.remote_path
    local_path = args.local_path
    for client in ftp_client_list:
      client.upload(remote_path, local_path)
  elif args.pull:
    remote_path = args.remote_path
    local_path = args.local_path
    for client in ftp_client_list:
      client.download(remote_path, local_path)
