def Reponse(code, msg, items,item):
    """
    This function Response for mapper reponse to user 
    :param  code    :       code of response
            msg     :       message for showing
            items   :       field for handle array data
            item    :       field for handle object data   
    """
    code = code
    message = msg
    items = items
    item = item
    response = {
        'code': code,
        'message': message,
        'items': items,
        'item': item,
    }
    
    return response