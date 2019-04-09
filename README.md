# Usage

### options

1. "-c": Use config file, must be a json format file,  see the config.example for example

2. "-d [remote_path]": delete file from ftp server @remote_path

3. "-u": Upload file mode

4. "-p": download file mode

5. "-r": set the remote path to be download or store uploaded file

6. "-l": set the local file path to be upload or to store download file

### examples:

1. upload 

``` shell

python3 ftp.py -c /home/user/Code/ftp/config -u -r /scripts3/mfiletransfer.py -l /home/user/Code/mfiletransfer/mfiletransfer.py

```

2. download

``` shell

python3 ftp.py -c /home/user/Code/ftp/config -p -r /scripts3/mfiletransfer.py -l /home/user/Code/mfiletransfer/mfiletransfer.py

```

3. delete

``` shell

python3 ftp.py -c /home/user/Code/ftp/config -d /scripts3/mfiletransfer.py

```


