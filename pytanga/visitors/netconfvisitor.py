from . import AbstractVisitor
import re
import xml.etree.ElementTree as ET


class VisitorError(Exception):
    pass


class NETCONFVisitor(AbstractVisitor):

    def parse(self, leaf):
        output = self.parseComponentData(leaf.tag, leaf.attributes, leaf.xmlns)
        for child in leaf.childrenData:
            output.append(child)
        return output

    def print(self, output):
        return ET.tostring(output, encoding='utf-8').decode()

    def parseComponentData(self, tag, data, xmlns):
        output = ET.Element(tag, **xmlns)
        for key in data:
            if((not isinstance(data[key], dict)) and
               (not isinstance(data[key], list))):
                child = ET.Element(key)
                child.text = data[key]
                output.append(child)
            elif (isinstance(data[key], list)):
                for value in data[key]:
                    child = ET.Element(key)
                    child.text = value
                    output.append(child)
            elif (isinstance(data[key], dict)):
                if('keys' in data[key]):
                    keys = data[key]['keys']
                    value = data[key]['value']
                    child = ET.Element(key, **keys)
                    child.text = value
                    if(key == 'identifier'):
                        output.insert(0, child)
                    else:
                        output.append(child)
                else:
                    child = ET.Element(key)
                    interDict = data[key]
                    for item in interDict:
                        if((not isinstance(interDict[item], dict)) and
                           (not isinstance(interDict[item], list))):
                            subChild = ET.Element(item)
                            subChild.text = interDict[item]
                            child.append(subChild)
                        elif (isinstance(interDict[item], list)):
                            for vaule in interDict[item]:
                                subChild = ET.Element(item)
                                subChild.text = value
                                child.append(subChild)
                        elif (isinstance(interDict[item], dict)):
                            if('keys' in interDict[item]):
                                extra = {}
                                extra = interDict[item]['keys']
                                subChild = ET.Element(item, **extra)
                                subChild.text = interDict[item]['value']
                                child.append(subChild)
                            else:
                                subChild = ET.Element(item)
                                t_interDict = interDict[item]
                                for t_item in t_interDict:
                                    if((not isinstance(t_interDict[t_item], dict)) and
                                       (not isinstance(t_interDict[t_item], list))):
                                        t_subChild = ET.Element(t_item)
                                        t_subChild.text = t_interDict[t_item]
                                        subChild.append(t_subChild)
                                    elif (isinstance(t_interDict[t_item], list)):
                                        for value in t_interDict[t_item]:
                                            t_subChild = ET.Element(t_item)
                                            t_subChild.text = value
                                            subChild.append(t_subChild)
                                    elif (isinstance(t_interDict[t_item], dict)):
                                        if('keys' in t_interDict[t_item]):
                                            extra = t_interDict[t_item]['keys']
                                            t_subChild = ET.Element(t_item, **extra)
                                            t_subChild.text = t_interDict[t_item]['value']
                                            subChild.append(t_subChild)
                                        else:
                                            raise VisitorError(
                                                "Too many nested levels, build a new module")
                                child.append(subChild)

                    output.append(child)
        return output

