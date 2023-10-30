
#LOGIC FOR REGISTERING FUNCTIONALITIES FROM VIEW IN JOURNAL. USING DECORATOR @register_activity
#for each view that wants to be register, must be first configurated here the way it would be display.
#Always satarts declaring an action = None and then return it with the activity message to be display in journal.
#If the registration is related to information that is being deleted form the DB, it must be configurated directly in the view.


def activity_staff_view(request, *args, **kwargs):
    action = None  # Start with None (if not registers everyithing)
    username = ""

    if "add_user" in request.POST:
        username = request.POST.get("username")
        action = f"User created: {username}"
    elif "delete_user" in request.POST:
        return None

    return action

def activity_edit_profile(request, *args, **kwargs):
    action = None
    
    if request.method == "POST":
        username = request.POST.get("username")
        action = f"User updated: {username}"

    return action