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

QUERY_CA_ATTRIBUTES = """SELECT 
aty.TypeName as Attribute, adt.TypeName as Type, ai.attribute as Integer, NULL as Text 
from Attribute a 
INNER JOIN attributedatatype adt ON ( a.attributedatatypeId = adt.attributedatatypeId and adt.typeName != 'Text') 
INNER JOIN attributeint ai ON (ai.attributeintId = a.attributedetailId) 
INNER JOIN attributetype aty ON (aty.attributeTypeId = ai.attributetypeId) 
where AttributeListId= {0} 
UNION 
SELECT aty.TypeName as Attribute, adt.TypeName as Type, NULL as Interger, at.attribute as Text 
from Attribute a 
INNER JOIN attributedatatype adt ON ( a.attributedatatypeId = adt.attributedatatypeId and adt.typeName == 'Text') 
INNER JOIN attributetext at ON (at.attributetextId = a.attributedetailId) 
INNER JOIN attributetype aty ON ( aty.attributeTypeId = at.attributetypeId) 
WHERE AttributeListId= {0};"""
