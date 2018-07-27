
JFLAGS = -g -d bin -sourcepath src 
JC = javac
RM = rm

SRCPATH = src/usersimproj

.SUFFIXES: .java .class

.java.class:
	$(JC) $(JFLAGS) $*.java

CLASSES = \
		$(SRCPATH)/CoreNLPWrap.java \
		$(SRCPATH)/StopwordAnnotator.java \
		$(SRCPATH)/DeSentence.java \
		$(SRCPATH)/DeToken.java \
		$(SRCPATH)/BabelWrap.java \
		$(SRCPATH)/ADWWrap.java \
		$(SRCPATH)/WordSimTask.java \
		$(SRCPATH)/WordSimServer.java \
		$(SRCPATH)/TestClient.java \
		$(SRCPATH)/UserSimTest.java 

default: classes

classes: $(CLASSES:.java=.class)

env:
	export CLASSPATH=./bin:${CLASSPATH}

clean:
	$(RM) -rf bin/*

