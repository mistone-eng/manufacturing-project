
ifeq ($(OS)$(os), Windows_NT)
	XCOMPILE := 1
	OS_PREFIX := C:
	OS_SUFFIX := .exe
	PYTHON := python
	MKDIR_P := $(PYTHON) ../../../../Platform/scripts/Utils/kUtil.py mkdir_p
	RM_F := $(PYTHON) ../../../../Platform/scripts/Utils/kUtil.py rm_f
	RM_RF := $(PYTHON) ../../../../Platform/scripts/Utils/kUtil.py rm_rf
	CP := $(PYTHON) ../../../../Platform/scripts/Utils/kUtil.py cp
else
	BUILD_MACHINE := $(shell uname -m)
	ifneq ($(BUILD_MACHINE), x86_64)
		XCOMPILE := 1
	else
		XCOMPILE := 0
	endif
	PYTHON := python3
	MKDIR_P := mkdir -p
	RM_F := rm -f
	RM_RF := rm -rf
	CP := cp
endif

TARGET_TRIPLET := x86_64-linux-gnu

ifeq ($(XCOMPILE),1)
	GCC_PATH := $(OS_PREFIX)/tools/GccX64_7.5.0-p3/$(TARGET_TRIPLET)
	GCC_SYSROOT := $(GCC_PATH)/$(TARGET_TRIPLET)/libc
	GCC_PREFIX := $(GCC_PATH)/bin/$(TARGET_TRIPLET)-
endif

GNU_C_COMPILER := $(GCC_PREFIX)gcc$(GCC_SLOT_SUFFIX)$(OS_SUFFIX)
GNU_CXX_COMPILER := $(GCC_PREFIX)g++$(GCC_SLOT_SUFFIX)$(OS_SUFFIX)
GNU_LINKER := $(GCC_PREFIX)g++$(GCC_SLOT_SUFFIX)$(OS_SUFFIX)
GNU_ARCHIVER := $(GCC_PREFIX)ar$(OS_SUFFIX)
GNU_READELF := $(GCC_PREFIX)readelf$(OS_SUFFIX)

KAPPGEN := $(PYTHON) ../../../../Platform/scripts/Utils/kAppGen.py

ifndef verbose
	SILENT := @
endif

ifndef config
	config := Debug
endif

# We require GCC to be installed according to specific conventions (see manuals).
# Tool prerequisites may change between major releases; check and report.
ifeq ($(shell $(GNU_C_COMPILER) --version),)
.PHONY: gcc_err
gcc_err:
	$(error Cannot build because of missing prerequisite; please install GCC)
endif

ifeq ($(config),Debug)
	optimize := 0
	strip := 0
	wstack := 0
	TARGET := ../../../bin/linux_x64d/AlignmentStationary
	INTERMEDIATES := 
	OBJ_DIR := ../../../build/AlignmentStationary-gnumk_linux_x64-Debug
	PREBUILD := 
	POSTBUILD := 
	COMPILER_FLAGS := -g -march=x86-64 -fpic -fvisibility=hidden
	C_FLAGS := -std=gnu99 -Wall -Wno-unused-variable -Wno-unused-parameter -Wno-unused-value -Wno-missing-braces
	CXX_FLAGS := -std=c++17 -Wall -Wfloat-conversion
	INCLUDE_DIRS := -I../../../Platform/kApi -I../../../Gocator/GoSdk
	DEFINES :=
	LINKER_FLAGS := -Wl,-no-undefined -Wl,--allow-shlib-undefined -Wl,-rpath,'$$ORIGIN/../../lib/linux_x64d' -Wl,-rpath-link,../../../lib/linux_x64d -Wl,--hash-style=gnu
	LIB_DIRS := -L../../../lib/linux_x64d
	LIBS := -Wl,--start-group -lkApi -lGoSdk -Wl,--end-group
	ifneq ($(optimize),0)
		COMPILER_FLAGS += -O$(optimize)
	endif
	ifeq ($(strip),1)
		LINKER_FLAGS += -Wl,--strip-debug
	endif
	ifeq ($(strip),2)
		LINKER_FLAGS += -Wl,--strip-all
	endif
	ifdef profile
		COMPILER_FLAGS += -pg
		LINKER_FLAGS += -pg
	endif
	ifdef coverage
		COMPILER_FLAGS += --coverage -fprofile-arcs -ftest-coverage
		LINKER_FLAGS += --coverage
		LIBS += -lgcov
	endif
	ifdef sanitize
		COMPILER_FLAGS += -fsanitize=$(sanitize)
		LINKER_FLAGS += -fsanitize=$(sanitize)
	endif
	GNU_COMPILER_FLAGS := $(COMPILER_FLAGS) -fno-gnu-unique
	ifneq ($(wstack),0)
		GNU_COMPILER_FLAGS += -Wstack-usage=$(wstack)
	endif
	OBJECTS := ../../../build/AlignmentStationary-gnumk_linux_x64-Debug/AlignmentStationary.c.o
	DEP_FILES = ../../../build/AlignmentStationary-gnumk_linux_x64-Debug/AlignmentStationary.c.d
	TARGET_DEPS = ./../../../lib/linux_x64d/libGoSdk.so

endif

ifeq ($(config),Release)
	optimize := 2
	strip := 1
	wstack := 0
	TARGET := ../../../bin/linux_x64/AlignmentStationary
	INTERMEDIATES := 
	OBJ_DIR := ../../../build/AlignmentStationary-gnumk_linux_x64-Release
	PREBUILD := 
	POSTBUILD := 
	COMPILER_FLAGS := -march=x86-64 -fpic -fvisibility=hidden
	C_FLAGS := -std=gnu99 -Wall -Wno-unused-variable -Wno-unused-parameter -Wno-unused-value -Wno-missing-braces
	CXX_FLAGS := -std=c++17 -Wall -Wfloat-conversion
	INCLUDE_DIRS := -I../../../Platform/kApi -I../../../Gocator/GoSdk
	DEFINES :=
	LINKER_FLAGS := -Wl,-no-undefined -Wl,--allow-shlib-undefined -Wl,-rpath,'$$ORIGIN/../../lib/linux_x64' -Wl,-rpath-link,../../../lib/linux_x64 -Wl,-O1 -Wl,--hash-style=gnu
	LIB_DIRS := -L../../../lib/linux_x64
	LIBS := -Wl,--start-group -lkApi -lGoSdk -Wl,--end-group
	ifneq ($(optimize),0)
		COMPILER_FLAGS += -O$(optimize)
	endif
	ifeq ($(strip),1)
		LINKER_FLAGS += -Wl,--strip-debug
	endif
	ifeq ($(strip),2)
		LINKER_FLAGS += -Wl,--strip-all
	endif
	ifdef profile
		COMPILER_FLAGS += -pg
		LINKER_FLAGS += -pg
	endif
	ifdef coverage
		COMPILER_FLAGS += --coverage -fprofile-arcs -ftest-coverage
		LINKER_FLAGS += --coverage
		LIBS += -lgcov
	endif
	ifdef sanitize
		COMPILER_FLAGS += -fsanitize=$(sanitize)
		LINKER_FLAGS += -fsanitize=$(sanitize)
	endif
	GNU_COMPILER_FLAGS := $(COMPILER_FLAGS) -fno-gnu-unique
	ifneq ($(wstack),0)
		GNU_COMPILER_FLAGS += -Wstack-usage=$(wstack)
	endif
	OBJECTS := ../../../build/AlignmentStationary-gnumk_linux_x64-Release/AlignmentStationary.c.o
	DEP_FILES = ../../../build/AlignmentStationary-gnumk_linux_x64-Release/AlignmentStationary.c.d
	TARGET_DEPS = ./../../../lib/linux_x64/libGoSdk.so

endif

.PHONY: all all-obj all-dep clean

all: $(OBJ_DIR)
	$(PREBUILD)
	$(SILENT) $(MAKE) -f AlignmentStationary-Linux_X64.mk all-dep
	$(SILENT) $(MAKE) -f AlignmentStationary-Linux_X64.mk all-obj

clean:
	$(SILENT) $(info Cleaning $(OBJ_DIR))
	$(SILENT) $(RM_RF) $(OBJ_DIR)
	$(SILENT) $(info Cleaning $(TARGET) $(INTERMEDIATES))
	$(SILENT) $(RM_F) $(TARGET) $(INTERMEDIATES)

all-obj: $(OBJ_DIR) $(TARGET)
all-dep: $(OBJ_DIR) $(DEP_FILES)

$(OBJ_DIR):
	$(SILENT) $(MKDIR_P) $@

ifeq ($(config),Debug)

$(TARGET): $(OBJECTS) $(TARGET_DEPS)
	$(SILENT) $(info LdX64 $(TARGET))
	$(SILENT) $(GNU_LINKER) $(OBJECTS) $(LINKER_FLAGS) $(LIBS) $(LIB_DIRS) -o$(TARGET)

endif

ifeq ($(config),Release)

$(TARGET): $(OBJECTS) $(TARGET_DEPS)
	$(SILENT) $(info LdX64 $(TARGET))
	$(SILENT) $(GNU_LINKER) $(OBJECTS) $(LINKER_FLAGS) $(LIBS) $(LIB_DIRS) -o$(TARGET)

endif

ifeq ($(config),Debug)

../../../build/AlignmentStationary-gnumk_linux_x64-Debug/AlignmentStationary.c.o ../../../build/AlignmentStationary-gnumk_linux_x64-Debug/AlignmentStationary.c.d: src/AlignmentStationary.c
	$(SILENT) $(info GccX64 src/AlignmentStationary.c)
	$(SILENT) $(GNU_C_COMPILER) $(GNU_COMPILER_FLAGS) $(C_FLAGS) $(DEFINES) $(INCLUDE_DIRS) -o ../../../build/AlignmentStationary-gnumk_linux_x64-Debug/AlignmentStationary.c.o -c src/AlignmentStationary.c -MMD -MP

endif

ifeq ($(config),Release)

../../../build/AlignmentStationary-gnumk_linux_x64-Release/AlignmentStationary.c.o ../../../build/AlignmentStationary-gnumk_linux_x64-Release/AlignmentStationary.c.d: src/AlignmentStationary.c
	$(SILENT) $(info GccX64 src/AlignmentStationary.c)
	$(SILENT) $(GNU_C_COMPILER) $(GNU_COMPILER_FLAGS) $(C_FLAGS) $(DEFINES) $(INCLUDE_DIRS) -o ../../../build/AlignmentStationary-gnumk_linux_x64-Release/AlignmentStationary.c.o -c src/AlignmentStationary.c -MMD -MP

endif

ifeq ($(MAKECMDGOALS),all-obj)

ifeq ($(config),Debug)

include ../../../build/AlignmentStationary-gnumk_linux_x64-Debug/AlignmentStationary.c.d

endif

ifeq ($(config),Release)

include ../../../build/AlignmentStationary-gnumk_linux_x64-Release/AlignmentStationary.c.d

endif

endif

