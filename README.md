# VS64 Developer Tools

VS64 Developer Tools Bundle.

## Special Note: Java Runtime Re-Distribution

The bundled JRE in this repository has been built to provide
the required environment for the KickAssembler Java application.

Detecting the required dependencies:

```
jdeps --list-deps KickAss.jar
```

This lists the following dependencies:

- java.base
- java.desktop
- java.xml

Generating the custom Java runtime:

```
jlink --no-header-files --no-man-pages --compress=zip-9 --strip-debug
      --add-modules java.base,java.desktop,java.xml
	  --output my_jre
```

The following JDK release has been used to generate the custom JRE:
(Taken from https://jdk.java.net/26)

```
IMPLEMENTOR="Oracle Corporation"
JAVA_RUNTIME_VERSION="26.0.1+8-34"
JAVA_VERSION="26.0.1"
JAVA_VERSION_DATE="2026-04-21"
OS_ARCH="x86_64"
OS_NAME="Windows"
SOURCE=".:git:fcc00fc4aee7"
```
