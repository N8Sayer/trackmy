import re

def ten(data,description=''):
    output = []
    if isinstance(data,dict):
        for attr,values in data.items():
            temp = ten(values,attr)
            if (temp and isinstance(temp[0],list)):
                for index, values in enumerate(temp):
                    output.append([description + ',' + values[0],values[1]])
            elif (temp and isinstance(temp[0],str)):
                output.append([description + ',' + temp[0],temp[1]])
    elif isinstance(data,list):
        for index,values in enumerate(data):
            if isinstance(values,str):
                output = [description, data]
            elif isinstance(values,dict):
                temp = ten(values,description)
                for index, values in enumerate(temp):
                    output.append(values)
            else:
                for lineValues in values:
                    if isinstance(lineValues[1],str):
                        output.append([description + ',' + lineValues[0], lineValues[1]])
                    elif isinstance(lineValues[1],dict):
                        temp = ten(lineValues[1],lineValues[0])
                        for index, values in enumerate(temp):
                            output.append([description + ',' + values[0],values[1]])
                    elif isinstance(lineValues[1],list):
                        temp = ten(lineValues[1],lineValues[0])
                        temp = [item for sublist in temp for item in sublist]
                        for index, values in enumerate(temp):
                            if (index % 2 == 0):
                                output.append([temp[index],temp[index+1]])
    elif isinstance(data,str):
        output = [description, str(data)]
    return output

##def traverse(obj, prev_path = "obj", path_repr = "{}[{}]"):
##    if isinstance(obj,dict):
##        it = obj.items()
##    elif isinstance(obj,list):
##        it = enumerate(obj)
##    else:
##        yield prev_path,obj
##        return
##    for key,value in it:
##        for data in traverse(value, path_repr.format(prev_path,key), path_repr):
##            yield data
