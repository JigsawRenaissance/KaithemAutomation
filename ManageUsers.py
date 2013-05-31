import cherrypy, auth ,pages

class ManageAuthorization():
    @cherrypy.expose
    def index(self):
        pages.require("/admin/users.edit")
        return pages.get_template("auth/index.html").render(auth = auth)
       
    #The actual POST target to delete a user
    @cherrypy.expose
    def deluser(self,**kwargs):
        pages.require("/admin/users.edit")
        auth.removeUser(kwargs['user'])
        raise cherrypy.HTTPRedirect("/auth")
    
	#POST target for deleting a group
    @cherrypy.expose
    def delgroup(self,**kwargs):
        pages.require("/admin/users.edit")
        auth.removeGroup(kwargs['group'])
        raise cherrypy.HTTPRedirect("/auth")
    
	#INterface to select a user to delete
    @cherrypy.expose
    def deleteuser(self,**kwargs):
        pages.require("/admin/users.edit")
        return pages.get_template("auth/deleteuser.html").render()
    
	#Interface to select a group to delete
    @cherrypy.expose
    def deletegroup(self,**kwargs):
        pages.require("/admin/users.edit")
        return pages.get_template("auth/deletegroup.html").render()
		
    #Add user interface
    @cherrypy.expose
    def newuser(self):
        pages.require("/admin/users.edit")
        return pages.get_template("auth/adduser.html").render()
		
    #add group interface       
    @cherrypy.expose
    def newgroup(self):
        pages.require("/admin/users.edit")
        return pages.get_template("auth/newgroup.html").render()
        
    @cherrypy.expose
    #handler for the POST request to change user settings
    def newusertarget(self,**kwargs):
        pages.require("/admin/users.edit")
        #create the new user
        auth.addUser(kwargs['username'],kwargs['password'])
        #Take the user back to the users page
        raise cherrypy.HTTPRedirect("/auth/")
            
        
    @cherrypy.expose
    #handler for the POST request to change user settings
    def newgrouptarget(self,**kwargs):
        pages.require("/admin/users.edit")
        #create the new user
        auth.addGroup(kwargs['groupname'])
        #Take the user back to the users page
        raise cherrypy.HTTPRedirect("/auth/")
            
    @cherrypy.expose
    #handler for the POST request to change user settings
    def updateuser(self,user,**kwargs):
        pages.require("/admin/users.edit")
        
		#Remove the user from all groups that the checkbox was not checked for
        for i in auth.Users[user]['groups']:
            if not ('Group'+i) in kwargs:
                auth.removeUserFromGroup(user,i)
            
        #Add the user to all checked groups
        for i in kwargs:
            if i[:5] == 'Group':
                if kwargs[i] == 'true':
                    auth.addUserToGroup(user,i[5:])
                    
        auth.changePassword(user,kwargs['password'])
        auth.changeUsername(user,kwargs['username'])
        #Take the user back to the users page
        raise cherrypy.HTTPRedirect("/auth")
   
    @cherrypy.expose
    #handler for the POST request to change user settings
    def updategroup(self,group,**kwargs):
        pages.require("/admin/users.edit")
        auth.Groups[group]['permissions'] = []
        #Handle all the group permission checkboxes
        for i in kwargs:
            if i[:10] == 'Permission':
                if kwargs[i] == 'true':
                    auth.addGroupPermission(group,i[10:])
                    
        #Take the user back to the users page
        auth.generateUserPermissions() #update all users to have the new permissions lists
        raise cherrypy.HTTPRedirect("/auth")
            
    #Settings page for one individual user    
    @cherrypy.expose
    def user(self,username):
        pages.require("/admin/users.edit")
        return pages.get_template("auth/user.html").render(
        usergroups=auth.Users[username]['groups'],
        groups= sorted(auth.Groups.keys()),
        password = auth.Users[username]['password'],
        username = username)
            
    #Settings page for one individual group    
    @cherrypy.expose
    def group(self,group):
        pages.require("/admin/users.edit")
        return pages.get_template("auth/group.html").render(
        auth = auth, name = group)
