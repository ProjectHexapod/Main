################################################################################
# Automatically-generated file. Do not edit!
################################################################################

#Progress monitor hint: 16
first : all
-include ../makefile.init

# This file contains definitions of environment variables used in the makefiles and .args files if exist.
-include makefile.local

RM := "$(Gnu_Make_Install_DirEnv)/rm" -f

# All of the sources participating in the build are defined here
-include sources.mk
-include subdir.mk
-include Sources/HIL/High\ Level\ Drivers/MAC/subdir.mk
-include Sources/HIL/High\ Level\ Drivers/High\ Level\ Start-up/subdir.mk
-include Sources/HAL/SPI/subdir.mk
-include Sources/HAL/SCI/subdir.mk
-include Sources/HAL/PHY/subdir.mk
-include Sources/HAL/MCG/subdir.mk
-include Sources/HAL/GPIO/subdir.mk
-include Sources/HAL/FLASH/subdir.mk
-include Sources/HAL/FEC/subdir.mk
-include Sources/HAL/ADC/subdir.mk
-include Sources/Applications/subdir.mk
-include Project\ Settings/Startup\ Code/subdir.mk
-include Libs/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C++_DEPS)),)
-include $(C++_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(CC_DEPS)),)
-include $(CC_DEPS)
endif
ifneq ($(strip $(CPP_DEPS)),)
-include $(CPP_DEPS)
endif
ifneq ($(strip $(CXX_DEPS)),)
-include $(CXX_DEPS)
endif
ifneq ($(strip $(C_UPPER_DEPS)),)
-include $(C_UPPER_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
Project.elf \

EXECUTABLES_QUOTED += \
"Project.elf" \

EXECUTABLES_OS_FORMAT += \
Project.elf \

_OUTPUTTYPE_NAME_BURNER_OUTPUT_OUTPUTS += \
Project.elf.s19 \

_OUTPUTTYPE_NAME_BURNER_OUTPUT_OUTPUTS_QUOTED += \
"Project.elf.s19" \

_OUTPUTTYPE_NAME_BURNER_OUTPUT_OUTPUTS_OS_FORMAT += \
Project.elf.s19 \


# All Target
call-burner := 0
ifneq ($(strip $(EXECUTABLES)),)
ifneq ($(strip $(BBL_SRCS_QUOTED)),)
call-burner := 1
endif
endif
ifeq ($(call-burner),1)
all: Project.elf Project.elf.s19
else
all: Project.elf
endif

# Tool invocations
Project.elf: $(OBJS) $(USER_OBJS) /home/jwhong/VMShared/Main/Firmware/BaseEthernetNode/prm/project_cw10.lcf
	@echo 'Building target: $@'
	@echo 'Executing target #17 $@'
	@echo 'Invoking: ColdFire Linker'
	"$(CF_ToolsDirEnv)/mwldmcf" @@"Project.args" -o "Project.elf"  $(USER_OBJS_QUOTED) $(LIBS_QUOTED)
	@echo 'Finished building target: $@'
	@echo ' '

Project.elf.s19: $(BBL_SRCS) $(EXECUTABLES)
	@echo 'Executing target #18 $@'
	@echo 'Invoking: Burner'
	"$(HC08ToolsEnv)/burner.exe"  -f="$<" -env"ABS_FILE=$(strip $(EXECUTABLES_OS_FORMAT))"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) "./*/*.obj" "./*/*/*.obj" "./*/*/*/*.obj" "./*/*/*/*/*.obj"  $(CPP_DEPS_QUOTED) $(CC_DEPS_QUOTED) $(_OUTPUTTYPE_NAME_BURNER_OUTPUT_OUTPUTS_QUOTED) $(CXX_DEPS_QUOTED) $(C_UPPER_DEPS_QUOTED) $(C++_DEPS_QUOTED) $(EXECUTABLES_QUOTED) "./*/*.d" "./*/*/*.d" "./*/*/*/*.d" "./*/*/*/*/*.d"  Project.elf
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY:

-include ../makefile.targets
