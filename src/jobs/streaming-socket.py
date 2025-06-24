import json 
import socket 
import time
import pandas as pd 
import os 

def handle_time(obj):
    if isinstance(obj,pd.Timestamp):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    return None

def send_data_to_socket(file_path, host="127.0.0.1", port=9999, chunk_size=100):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    #allow one client to wait in the queue
    s.listen(1)
    print("Server is listening")

    #connect to client, ensure server is alawys on -> put in loop
    last_index=0

    while True:

        conn,adr = s.accept()
        print("Connected to client")

        try:
            with open(file_path,"r") as file:
                records =[]

                #skip the rows were sent before
                for _ in range(last_index):
                    next(file) #read the next line
                
                #after skipping, go for the remain file
                for line in file:
                    records.append(json.loads(line.strip()))
                    if len(records) == chunk_size:
                        #convert one by one 
                        for record in records:
                            print("Encoding records: ",record)
                            chunk_json = json.dumps(record, default=handle_time).encode("utf-8")
                            conn.send(chunk_json+b"\n")
                            last_index +=1
                            time.sleep(2) #allow delay
                                    
                        records=[]
                        
                if records:
                    for record in records:
                            print("Encoding records: ",record)
                            chunk_json = json.dumps(record, default=handle_time).encode("utf-8")
                            conn.send(chunk_json+b"\n")
                

        except Exception as e:
            print(f"Error: ", e)

        finally:
            #close server 
            conn.close()

if __name__ == "__main__":
    file_path = "../datasets/yelp_academic_dataset_review.json"
    abs_path = os.path.abspath(file_path)
    print(f"File path: ", abs_path)
    send_data_to_socket(abs_path)

