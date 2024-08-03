''' Module to hold all databae statements in one place '''



QUERY_COMPLEX_ACTION = """SELECT 
ca.complexactionid as ActionId_Parent,  
ert.typename as Rule_TypeName_Parent, 
er.attributelistid as Rule_AttributeListId_Parent, 
ca.attributelistid  as Attributelistid_Parent, 
child_a.actionid  as ActionId_Child, 
child_a.actiondetailid as ActionDetailId_Child, 
at.shortname as ActionType_Child, 
mt.paramIdentifier as mediatype_Child, 
child_a.sequenceListId as sequenceListId_Child 
FROM action parent_a 
INNER JOIN complexaction ca ON parent_a.actiondetailid = ca.complexactionid 
LEFT JOIN executionrule er ON ca.executionruleid = er.executionruleid 
LEFT JOIN executionruletype ert ON er.executionruletypeid = ert.executionruletypeid 
LEFT JOIN complexactionchildlist cacl ON ca.complexactionid = cacl.complexactionid 
LEFT JOIN action child_a ON cacl.actionid = child_a.actionId 
LEFT JOIN mediatype mt ON mt.mediatypeId = child_a.mediatypeid 
LEFT JOIN actiontype at ON child_a.actiontypeid = at.actiontypeid 
WHERE parent_a.actionid = {0} 
ORDER BY cacl.orderindex;"""