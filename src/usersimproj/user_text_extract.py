import json
import sys

filtered_json_data = []

# Description:
#   This function reads in a json file, then parses it line by line.
#   Each line is a json record. The output is of the form as follows:
#   {"user" : "USER LOGIN ID", "created_at" : "TIMESTAMP OF THIS TEXT",
#   "type" : "TYPE OF THIS EVENT", "text_str" : "TEXT CONTENT"}
def read_json_file(file_name):
    #ln_num = 1
    with open(file_name, 'r') as in_file:
        in_file.seek(0, 0)
        for line in in_file:
            json_line_data = json.loads(line)
            filtered_json_line_data = {key:val for (key, val) in json_line_data.items()
                                       if key == "actor" or key == "created_at" or key == "payload" or key == "type"}

            filtered_json_line_data.update({"user" : filtered_json_line_data["actor"]["login_h"]})

            if filtered_json_line_data["type"] == "CommitCommentEvent":
                filtered_json_line_data.update({"text_m" : filtered_json_line_data["payload"]["comment"]["body_m"]})
            elif filtered_json_line_data["type"] == "CreateEvent":
                filtered_json_line_data.update({"text_m" : filtered_json_line_data["payload"]["description_m"]})
            elif filtered_json_line_data["type"] == "IssueCommentEvent":
                filtered_json_line_data.update({"text_m" : filtered_json_line_data["payload"]["comment"]["body_m"]})
            elif filtered_json_line_data["type"] == "IssuesEvent":
                filtered_json_line_data.update({"text_m" : filtered_json_line_data["payload"]["issue"]["body_m"]})
            # there may be a chance that no "body_m" exists in this event, which is not consistent with the doc.
            elif filtered_json_line_data["type"] == "PullRequestEvent" \
                and filtered_json_line_data["payload"]["pull_request"].has_key("body_m"):
                filtered_json_line_data.update({"text_m" : filtered_json_line_data["payload"]["pull_request"]["body_m"]})
            # elif filtered_json_line_data["type"] == "PushEvent":
            #     for commit in filtered_json_line_data["payload"]["commits"]:
            #         print commit
            elif filtered_json_line_data["type"] == "ReleaseEvent":
                filtered_json_line_data.update({"text_m" : filtered_json_line_data["payload"]["release"]["body_m"]})
            elif filtered_json_line_data["type"] == "PullRequestReviewCommentEvent":
                filtered_json_line_data.update({"text_m" : filtered_json_line_data["payload"]["comment"]["body_m"]})
            else:
                filtered_json_line_data.update({"text_m" : ""})

            del filtered_json_line_data["payload"]
            del filtered_json_line_data["actor"]
            # del filtered_json_line_data["type"]

            # print "ln:" + str(ln_num)
            # print filtered_json_line_data
            # print "\n"
            # ln_num += 1

            if filtered_json_line_data["text_m"] != "":
                filtered_json_data.append(filtered_json_line_data)
        #print(filtered_json_data)
        in_file.close()

def write_json_file(file_name):
    with open(file_name, 'w') as out_file:
        out_file.seek(0, 0)
        for item in filtered_json_data:
            json_out_line_data = json.dumps(item)
            out_file.write(json_out_line_data + '\n')
        out_file.close()

def main():
    for arg in sys.argv[1:]:
        print(arg)
        read_json_file(arg)
        #print(filtered_json_data)
    output_name = input("Please input output json file name:")
    write_json_file(output_name)

main()

