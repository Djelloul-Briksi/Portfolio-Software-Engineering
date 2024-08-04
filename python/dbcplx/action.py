''' Module to handle database actions, incl. complex actions '''


import db_queries


class Action():
    ''' Class to hold an action '''

    def __init__(self, act_id, act_list_id, act_det_id, act_typ, med_typ):
        '''
        Constructor
        act_id: action id (database: action.ActionID)
        act_list_id: action list id (database: action.ActionListID)
        act_det_id: action detail id (database: action.ActionDetailID)
        act_typ: action type as string (database: actiontype.ShortName)
        med_typ: media type as string (database: mediatype.ParamIdentifier)
        '''
        self.act_id = act_id
        self.act_list_id = act_list_id
        self.act_det_id = act_det_id
        self.act_typ = act_typ
        self.med_typ = med_typ
        self.typ = act_typ   # this type is overwritten for complex action (e.g. 'Serial' instead of 'CAStatic')

        self.children = []
        self.attributes = []
        self.tree = dict()

    def addChild(self, action):
        '''
        Add a child action to the current (parent) action
        action: action object to add
        '''
        self.children.append(action)

    def buildTree(self):
        ''' Build the action data (content) tree (dictionnary) '''
        self.tree['type'] = self.typ
        self.tree['actionId'] = self.act_id
        self.tree['actionDetailId'] = self.act_det_id
        self.tree['actionType'] = self.act_typ
        self.tree['mediaType'] = self.med_typ

        for attr in self.attributes:
            for key, value in attr.items():
                if key in self.tree:
                    # append to existing attribute
                    self.tree[key] = str("{0}, {1}").format(self.tree[key], value)
                else:
                    # create new attribute
                    self.tree[key] = value

        self.tree['children'] = []
        for action in self.children:
            action.buildTree()
            self.tree['children'].append(action.tree)
        
        return self.tree


class DbAction():
    ''' Class to handle database actions, incl. complex actions '''

    def __init__(self, db_conn):
        '''
        Constructor
        db_conn: database connection object (sqlite3)
        '''
        self.db_conn = db_conn

    def getAction(self, action: Action):
        '''
        Get action (tree) for the give action.
        action: action object
        '''
        print("getAction: ", action.act_typ)

        if (action.act_typ == "CAStatic"):
            self.getComplexAction(action)

    def getComplexAction(self, action: Action):
        '''
        Get action tree for the given complex action
        action: complex action object
        '''
        cursor = self.db_conn.execute(str(db_queries.QUERY_COMPLEX_ACTION).format(action.act_id))
        for row in cursor:
            print("getComplexAction: row={0}".format(row))

            # overwrite the action type (write e.g. 'Serial' instead of 'CAStatic')
            action.typ = row[1]

            # get rule attributes
            self.getCAAttributes(row[2], action)

            # get complex action attributes
            self.getCAAttributes(row[3], action)

            child_action = Action(row[4], action.act_list_id, row[5], row[6], row[7])
            self.getAction(child_action)
            action.addChild(child_action)

    def getCAAttributes(self, attrListId, action: Action):
        '''
        Get the list of attributes of the given complex action 
        attrListId: attributes list id
        action: complex action
        '''
        if attrListId is not None:
            cursor = self.db_conn.execute(str(db_queries.QUERY_CA_ATTRIBUTES).format(attrListId))
            for row in cursor:
                print("getCAAttributes: row={0}".format(row))
                attr = dict()
                if row[1] == 'Integer':
                    attr[row[0]] = row[2]
                elif row[1] == 'Text':
                    attr[row[0]] = row[3]
                action.attributes.append(attr)

def getActionTree(root_action : Action, db_conn):
    '''
    '''
    my_dbaction = DbAction(db_conn)
    my_dbaction.getAction(root_action)
    return root_action.buildTree()
