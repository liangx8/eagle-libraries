import xml.etree.ElementTree as et

def itr(top,tagName,fn):
    for child in top:
        if child.tag == tagName:
            fn(child)
        else:
            itr(child,tagName,fn)
def itrAll(top,fn,lvl):
    fn(top,lvl)
    for child in top:
        itrAll(child,fn,lvl+1)
class XmlHelper():
    def __init__(self,fn):
        self.__readfile=fn
        self.__tree=et.parse(fn)
        self.__jobs=list()
        # root=self.__tree.getroot()
    def getroot(self):
        return self.__tree.getroot()
    def findTag(self,tagName,fn):
        itr(self.__tree.getroot(),tagName,fn)
    def walk(self):
        def fn(node,lvl):
            for job in self.__jobs:
                job(node,lvl)
        itrAll(self.__tree.getroot(),fn,0)
    def addJob(self,job):
        self.__jobs.append(job)
    def save(self,file=None):
        if file == None:
            self.__tree.write(self.__readfile)
        else:
            self.__tree.write(file)
        
            
    def outline(self,x1,y1,x2,y2):
        root=self.__tree.getroot()
        plain=None
        for b in root.iter('plain'):
            if plain == None:
                plain=b
            else:
                raise Exception("there are multple <plain> tag")
        if plain == None:
            raise Exception('<board> tag is not found')
        wires = plain.findall('wire')
        if len(wires) != 4:
            raise Exception('expecet 4 wire tag')
        sx1=str(x1)
        sx2=str(x2)
        sy1=str(y1)
        sy2=str(y2)
        def setRect(attr,a,b,c,d):
            attr['x1']=a
            attr['y1']=b
            attr['x2']=c
            attr['y2']=d
        setRect(wires[0].attrib,sx1,sy1,sx2,sy1)
        setRect(wires[1].attrib,sx1,sy1,sx1,sy2)
        setRect(wires[2].attrib,sx1,sy2,sx2,sy2)
        setRect(wires[3].attrib,sx2,sy1,sx2,sy2)
        for w in wires:
            print(w.attrib)
    


if __name__=="__main__":
    h=XmlHelper('/home/arm/EAGLE/projects/bmc/bmc.brd')
    def prt(e):
        print(e.attrib)
    
    print('find package')
    h.findTag('package',prt)
    
    print('find symbol')
    h.findTag('symbol',prt)

    print('find gate')
    h.findTag('gate',prt)

    print('-------------------all')
    def byName(node,lvl):
        if lvl > 0:
            print('  ' * lvl,end="")
        print(node.tag,end=": ")
        if node.tag == 'wire' or node.tag=='board':
            print(node.attrib)
        else:
            print("n/a")
    h.addJob(byName)
    #h.walk()
    h.outline(0,0,100,100)
    h.save()
