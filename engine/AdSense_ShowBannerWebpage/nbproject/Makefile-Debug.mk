#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Environment
MKDIR=mkdir
CP=cp
GREP=grep
NM=nm
CCADMIN=CCadmin
RANLIB=ranlib
CC=gcc
CCC=g++
CXX=g++
FC=gfortran
AS=as

# Macros
CND_PLATFORM=GNU-Linux
CND_DLIB_EXT=so
CND_CONF=Debug
CND_DISTDIR=dist
CND_BUILDDIR=build

# Include project Makefile
include Makefile

# Object Directory
OBJECTDIR=${CND_BUILDDIR}/${CND_CONF}/${CND_PLATFORM}

# Object Files
OBJECTFILES= \
	${OBJECTDIR}/mainAdSenseShowBannerWebpage.o


# C Compiler Flags
CFLAGS=

# CC Compiler Flags
CCFLAGS=
CXXFLAGS=

# Fortran Compiler Flags
FFLAGS=

# Assembler Flags
ASFLAGS=

# Link Libraries and Options
LDLIBSOPTIONS=-lcgicc ../AdEngine/build/Debug/GNU-Linux/AdEngine.a -lhiredis -lcurl -lpthread -ldl -ljansson

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-${CND_CONF}.mk ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/adsense_showbannerwebpage

${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/adsense_showbannerwebpage: ../AdEngine/build/Debug/GNU-Linux/AdEngine.a

${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/adsense_showbannerwebpage: ${OBJECTFILES}
	${MKDIR} -p ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}
	${LINK.cc} -o ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/adsense_showbannerwebpage ${OBJECTFILES} ${LDLIBSOPTIONS}

${OBJECTDIR}/mainAdSenseShowBannerWebpage.o: mainAdSenseShowBannerWebpage.cpp 
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -include ../AdEngine/AdEngine.hpp -std=c++11 -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/mainAdSenseShowBannerWebpage.o mainAdSenseShowBannerWebpage.cpp

# Subprojects
.build-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r ${CND_BUILDDIR}/${CND_CONF}
	${RM} ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/adsense_showbannerwebpage

# Subprojects
.clean-subprojects:

# Enable dependency checking
.dep.inc: .depcheck-impl

include .dep.inc