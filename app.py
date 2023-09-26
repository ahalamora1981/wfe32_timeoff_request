import json
import streamlit as st
import pandas as pd

from package.wfe32 import get_token, get_org_id, get_timeoff
from package.wfe32 import get_an_employee, process_timeoff_request


USERNAME = "jtao"
PASSWORD = "verint1!"
ORG_NAME = "Customer Service Team 3"
STATUS_CODE = 1

# Status                  Code
# Pending --------------- 1
# Approved -------------- 2
# Denied ---------------- 4
# Escalated ------------- 8
# Negotiation ----------- 16
# Tentative ------------- 32
# Invalid --------------- 64
# Withdrawn ------------- 128
# Waitlist -------------- 256
# Withdraw Request ------ 512
# Withdraw Reject ------- 1024
# Withdraw Cancel ------- 2048
# Withdraw Accept ------- 4096
# Withdraw Negotiation -- 8192

if __name__ == "__main__":

    st.set_page_config(page_title="VERINT", page_icon="resource/v_logo.png")

    st.image("resource/verint_logo.png", width=300)
    st.title("Timeoff Requests")

    if "timeoff" not in st.session_state:

        st.session_state["token"] = get_token(username=USERNAME, password=PASSWORD)

        st.session_state["org_id"] = get_org_id(st.session_state["token"], org_name=ORG_NAME)

        st.session_state["timeoff"] = get_timeoff(st.session_state["token"], st.session_state["org_id"], status=STATUS_CODE)

    data = {
        "Employee Name": [],
        "Request Status": [],
        "Submitted Time": [],
        "Start Time": [],
        "End Time": []
    }

    for timeoff_req in st.session_state["timeoff"]["timeoffRequest"]:

        request_id = timeoff_req["id"]

        employee_id = timeoff_req["employeeId"]
        employee = get_an_employee(st.session_state["token"], employee_id)
        person = employee["data"]["attributes"]["person"]
        first_name = person["firstName"]
        last_name = person["lastName"]

        data["Employee Name"].append(f"{first_name} {last_name}")
        data["Request Status"].append(str(timeoff_req["statusHistory"][0]["status"]))
        data["Submitted Time"].append(str(timeoff_req["submittedOn"]))
        data["Start Time"].append(str(timeoff_req["startTime"]))
        data["End Time"].append(str(timeoff_req["endTime"]))

    df = pd.DataFrame.from_dict(data, orient = 'index', columns=[f"Request #{i+1}" for i in range(len(data["Employee Name"]))])

    st.dataframe(df)

    if st.session_state["timeoff"]["timeoffRequest"]:

        request_num = st.selectbox("Please select the Request #", [f"Request #{i+1}" for i in range(len(data["Employee Name"]))])

        action = st.radio("Please select the Action", ["Approve", "Tentatively Approve", "Deny"])

        if st.button("Process the Action"):
            if action == "Approve":
                action_code = 10
                response = process_timeoff_request(st.session_state["token"], request_id, action_code)
                st.write(response["timeOffRequest"]["statusHistory"][-1])

            elif action == "Tentatively Approve":
                action_code = 9
                response = process_timeoff_request(st.session_state["token"], request_id, action_code)
                st.write(response["timeOffRequest"]["statusHistory"][-1])

            elif action == "Deny":
                action_code = 5
                response = process_timeoff_request(st.session_state["token"], request_id, action_code)
                st.write(response["timeOffRequest"]["statusHistory"][-1])

            st.session_state["timeoff"] = get_timeoff(st.session_state["token"], st.session_state["org_id"], status=STATUS_CODE)
