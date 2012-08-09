/******************************************************************************
*                                                  
*  (c) copyright Freescale Semiconductor 2008
*  ALL RIGHTS RESERVED
*
*  File Name:   Fat.c
*                                                                          
*  Description: Fat16 lite driver 
*                                                                                     
*  Assembler:   Codewarrior for HC(S)08 V6.1
*                                            
*  Version:     1.1                                                         
*                                                                                                                                                         
*  Author:      Jose Ruiz (SSE Americas)
*                                                                                       
*  Location:    Guadalajara,Mexico                                              
*                                                                                                                  
*                                                  
* UPDATED HISTORY:
*
* REV   YYYY.MM.DD  AUTHOR        DESCRIPTION OF CHANGE
* ---   ----------  ------        --------------------- 
* 1.0   2008.02.18  Jose Ruiz     Initial version
* 1.1   2008.05.02  Jose Ruiz     Initial version
* 1.2   2009.03.16  Mr Alcantara  Changed functions to be re-entrant.
*                                 Removed casting issues
*                                 Upgraded endian function depending on target
* 1.3   2009.05.13  Mr Alcantara  Releasing LS command to list files
* 1.3   2009.07.02  Mr Alcantara  LS command fixes
* 
******************************************************************************/                                                                        
/* Freescale  is  not  obligated  to  provide  any  support, upgrades or new */
/* releases  of  the Software. Freescale may make changes to the Software at */
/* any time, without any obligation to notify or provide updated versions of */
/* the  Software  to you. Freescale expressly disclaims any warranty for the */
/* Software.  The  Software is provided as is, without warranty of any kind, */
/* either  express  or  implied,  including, without limitation, the implied */
/* warranties  of  merchantability,  fitness  for  a  particular purpose, or */
/* non-infringement.  You  assume  the entire risk arising out of the use or */
/* performance of the Software, or any systems you design using the software */
/* (if  any).  Nothing  may  be construed as a warranty or representation by */
/* Freescale  that  the  Software  or  any derivative work developed with or */
/* incorporating  the  Software  will  be  free  from  infringement  of  the */
/* intellectual property rights of third parties. In no event will Freescale */
/* be  liable,  whether in contract, tort, or otherwise, for any incidental, */
/* special,  indirect, consequential or punitive damages, including, but not */
/* limited  to,  damages  for  any loss of use, loss of time, inconvenience, */
/* commercial loss, or lost profits, savings, or revenues to the full extent */
/* such  may be disclaimed by law. The Software is not fault tolerant and is */
/* not  designed,  manufactured  or  intended by Freescale for incorporation */
/* into  products intended for use or resale in on-line control equipment in */
/* hazardous, dangerous to life or potentially life-threatening environments */
/* requiring  fail-safe  performance,  such  as  in the operation of nuclear */
/* facilities,  aircraft  navigation  or  communication systems, air traffic */
/* control,  direct  life  support machines or weapons systems, in which the */
/* failure  of  products  could  lead  directly to death, personal injury or */
/* severe  physical  or  environmental  damage  (High  Risk Activities). You */
/* specifically  represent and warrant that you will not use the Software or */
/* any  derivative  work of the Software for High Risk Activities.           */
/* Freescale  and the Freescale logos are registered trademarks of Freescale */
/* Semiconductor Inc.                                                        */ 
/*****************************************************************************/

/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

/* Includes */
#include "Fat.h"
#include "SD.h"
#include "stdlib.h"
#include "cf_board.h"

/*Local Variable holding FAT info*/
static FATHandler FATLocalhandle;
static uint8 sd_configured = FALSE;

/**
 * Start SDcard with FAT16 support
 *
 * @param none
 * @return FAT handler
 */
FATHandler*
FAT_INIT(UINT8 *u8FATReadBuffer)
{    
    FATHandler *sd_handler;
    
    if( sd_configured == FALSE )
    {
       if( SD_Init() == OK )
       {
         /*FAT init*/
         sd_handler = FAT_Read_Master_Block(u8FATReadBuffer);
         /*configured*/
         sd_configured = TRUE;
       }
       else
       {
         /*error*/
         sd_handler = NULL;
       }
    }
    else
    {
       /*already configured*/
       sd_handler = &FATLocalhandle;
    }

fat_init_exit:
    /*return handler in either case*/
    return sd_handler;  
}

/**
 * Stop SDcard with FAT16 support
 *
 * @param none
 * @return none
 */
void
FAT_Close()
{        
    sd_configured = FALSE;
}

/***************************************************************************************/
FATHandler*
FAT_Read_Master_Block(UINT8 *u8FATReadBuffer)
{
    MasterBoot_Entries *pMasterBoot;
    FATHandler *FAThandle;    

    /*FAT global assignation*/
    FAThandle = &FATLocalhandle;

    /*FSL:added lines*/
    FAThandle->u16Main_Offset=0;

    while(u8FATReadBuffer[0]!= 0xEB && u8FATReadBuffer[1]!=0x3C && u8FATReadBuffer[2]!=0x90) 
    {
        GetPhysicalBlock(FAThandle->u16Main_Offset++,&u8FATReadBuffer[0]);
    }
    FAThandle->u16Main_Offset--;

    pMasterBoot=(MasterBoot_Entries*)u8FATReadBuffer;
    FAThandle->u16FAT_Cluster_Size=pMasterBoot->SectorsPerCluster;
    FAThandle->u16FAT_Sector_Size=ByteSwap(pMasterBoot->BytesPerSector);
    FAThandle->u16FAT_FAT_BASE=  FAThandle->u16Main_Offset+ByteSwap(pMasterBoot->ReservedSectors);
    FAThandle->u16FAT_Root_BASE= (ByteSwap(pMasterBoot->SectorsPerFat)<<1)+FAThandle->u16FAT_FAT_BASE;
    FAThandle->u16FAT_Data_BASE= (ByteSwap(pMasterBoot->RootDirectoryEntries) >>4)+FAThandle->u16FAT_Root_BASE;
 
    /*Create mutex once*/
    FAThandle->FAT_Mutex = (void *)xSemaphoreCreateMutex();
    
    return FAThandle;
}
/***************************************************************************************/

/***************************************************************************************/
UINT8 
FAT_LS(FATHandler *FAThandle,UINT8 *u8FATReadBuffer,void *OUTHandle,UINT8 (*send_func)(void*,UINT8*))
{
    UINT8 u8Counter,u8Counter2;
    UINT8 u8BlockOffset=0;
    UINT8 u8BlockCounter=1;
    //UINT16 u16FileCounter=0;
    UINT8 fileName[FAT_NAME_LENGTH];
    root_Entries *sFileStructure;                                   
    
    GetPhysicalBlock(FAThandle->u16FAT_Root_BASE,u8FATReadBuffer);
    sFileStructure = (root_Entries*)u8FATReadBuffer;
#if 0/*No volume name info needed*/
    for(u8Counter=0;u8Counter<8;u8Counter++)
        if(sFileStructure->FileName[u8Counter]!=' ')
            //send volume information
#endif        
    sFileStructure++;
    
    while(sFileStructure->FileName[0]!=FILE_Clear)
    {
        if(sFileStructure->FileName[0]!=FILE_Erased)
        {
            //u16FileCounter++;
            for(u8Counter=0;u8Counter<8;u8Counter++)
            {
                if(sFileStructure->FileName[u8Counter]!=' ')
                    fileName[u8Counter] = sFileStructure->FileName[u8Counter];
                else
                    break;
            }
            fileName[u8Counter++] = '.';/*dot delimitator*/
            for(u8Counter2=0;u8Counter2<3;u8Counter2++)
            {
                if(sFileStructure->Extension[u8Counter2]!=' ')
                    fileName[u8Counter+u8Counter2] = sFileStructure->Extension[u8Counter2];
                else
                    break;
            }
            /*close the string*/
            fileName[u8Counter+u8Counter2] = NULL;/*string delimitator*/
            
            /*send to proposed callback function that will handle the string*/            
            if(!send_func(OUTHandle,(UINT8*)fileName) )
            {
              return 0;/*stop it*/
            }
        }
        u8BlockCounter++;
        sFileStructure++;    
        if(u8BlockCounter == FAT16_MAX_FILES)
        {
            u8BlockOffset++;
            GetPhysicalBlock(FAThandle->u16FAT_Root_BASE+u8BlockOffset,u8FATReadBuffer);
            sFileStructure = (root_Entries*)u8FATReadBuffer;
            u8BlockCounter=0;
        }
    }
    return 1;/*no error*///u16FileCounter;
}


/***************************************************************************************/
void 
FAT_FileClose(FATHandler *FAThandle,UINT8 *u8FATReadBuffer)
{
    root_Entries *sFileStructure;
    UINT16 *pu16FATPointer;
    UINT8 u8Counter;
    UINT32 u32Sector;
    UINT16 u16Offset;   

    /* Directory Entry*/
    u32Sector=FAThandle->WHandler.Dir_Entry/(FAThandle->u16FAT_Sector_Size>>5);
    u16Offset=FAThandle->WHandler.Dir_Entry%(FAThandle->u16FAT_Sector_Size>>5);
    
    GetPhysicalBlock(FAThandle->u16FAT_Root_BASE+u32Sector,u8FATReadBuffer);
    sFileStructure=(root_Entries*)u8FATReadBuffer;
    sFileStructure+=u16Offset;

    // FileName
    for(u8Counter=0;u8Counter<8;u8Counter++)
        sFileStructure->FileName[u8Counter]=FAThandle->WHandler.FileName[u8Counter];

    // Entension
    for(u8Counter=0;u8Counter<3;u8Counter++)
        sFileStructure->Extension[u8Counter]=FAThandle->WHandler.Extension[u8Counter];


    // Attributes
    sFileStructure->Attributes=0x20;
    sFileStructure->_Case=0x18;
    sFileStructure->MiliSeconds=0xC6;
    
    // Date & Time Information
    sFileStructure->CreationTime=0x2008;
    sFileStructure->CreationDate=0x2136;
    sFileStructure->AccessDate=0x2136;
    sFileStructure->ModificationTime=0x2008;
    sFileStructure->ModificationDate=0x2136;
    
    // Fat entry and file Size
    sFileStructure->ClusterNumber=ByteSwap(FAThandle->WHandler.BaseFatEntry);
    
    sFileStructure->SizeofFile=LWordSwap(FAThandle->WHandler.File_Size); 

    StorePhysicalBLock(FAThandle->u16FAT_Root_BASE+u32Sector,u8FATReadBuffer);
    
    /* FAT Table */
    u32Sector=FAThandle->WHandler.CurrentFatEntry/(FAThandle->u16FAT_Sector_Size>>1);
    u16Offset=FAThandle->WHandler.CurrentFatEntry%(FAThandle->u16FAT_Sector_Size>>1);

    GetPhysicalBlock(FAThandle->u16FAT_FAT_BASE+u32Sector,u8FATReadBuffer);
    
    pu16FATPointer=(UINT16*)u8FATReadBuffer;
    pu16FATPointer+=u16Offset;
    *pu16FATPointer=0xFFFF;     // Write Final Cluster    

    StorePhysicalBLock(FAThandle->u16FAT_FAT_BASE+u32Sector,u8FATReadBuffer);
}

/***************************************************************************************/
UINT16 
FAT_SearchAvailableFAT(FATHandler *FAThandle,UINT8 *u8FATReadBuffer,UINT16 u16CurrentFAT)
{
    UINT16 *pu16DataPointer;
    UINT16 u16FatEntry=0;
    UINT16 u16Sector=0;
    UINT16 u16byteSector;
    
    u16Sector=FAThandle->u16FAT_FAT_BASE;
    while(u16Sector < (((FAThandle->u16FAT_Root_BASE-FAThandle->u16FAT_FAT_BASE)>>1)+FAThandle->u16Main_Offset))
    {        GetPhysicalBlock(u16Sector++,u8FATReadBuffer);
        pu16DataPointer=(UINT16*)u8FATReadBuffer;
        u16byteSector=0;
        
        while(u16byteSector<FAThandle->u16FAT_Sector_Size)
        {
            if(*pu16DataPointer==0x0000)
                if(u16FatEntry!=u16CurrentFAT)
                    return(u16FatEntry);
            pu16DataPointer++;
            u16FatEntry++;
            u16byteSector++;
        }
    }
    return(0);  // Return 0 if no more FAT positions available
}

/***************************************************************************************/
UINT16 
FAT_Entry(FATHandler *FAThandle,UINT8 *u8FATReadBuffer,UINT16 u16FatEntry,UINT16 u16FatValue, UINT8 u8Function)
{
    UINT16 *pu16DataPointer;
    
    UINT16 u16Block;
    UINT8 u8Offset;
    
    u16Block = u16FatEntry / (FAThandle->u16FAT_Sector_Size>>1);
    u8Offset = (UINT8)(u16FatEntry % (FAThandle->u16FAT_Sector_Size >>1));

    GetPhysicalBlock(FAThandle->u16FAT_FAT_BASE+u16Block,u8FATReadBuffer);
    pu16DataPointer=(UINT16*)u8FATReadBuffer;
    pu16DataPointer+=u8Offset;

    if(u8Function==NEXT_ENTRY)
        return(ByteSwap(*pu16DataPointer));
    
    if(u8Function==WRITE_ENTRY)
    {
        *pu16DataPointer=ByteSwap(u16FatValue);
        StorePhysicalBLock(FAThandle->u16FAT_FAT_BASE+u16Block,u8FATReadBuffer);
        return(0x00);
    }
                
}

/***************************************************************************************/
void 
FAT_FileWrite(FATHandler *FAThandle,UINT8 *u8FATReadBuffer,UINT8 *pu8DataPointer,UINT32 u32Size)
{
    UINT32 u32SectorToWrite;
    UINT8 *pu8ArrayPointer;
    UINT16 u16TempFat;
    UINT8  u8ChangeSector=1;

    while(u32Size)
    {
        if(u8ChangeSector)
        {
            u32SectorToWrite= FAThandle->u16FAT_Data_BASE + FAThandle->WHandler.ClusterIndex + (FAThandle->WHandler.CurrentFatEntry-2)*FAThandle->u16FAT_Cluster_Size;
            GetPhysicalBlock(u32SectorToWrite,u8FATReadBuffer); 
            pu8ArrayPointer=u8FATReadBuffer+FAThandle->WHandler.SectorIndex;
            u8ChangeSector=0;
        }
        
        while(FAThandle->WHandler.SectorIndex<FAThandle->u16FAT_Sector_Size  &&  u32Size)
        {
            u32Size--;    
            FAThandle->WHandler.SectorIndex++;
            FAThandle->WHandler.File_Size++;
            *pu8ArrayPointer++=*pu8DataPointer++;    
        }
        
        StorePhysicalBLock(u32SectorToWrite,u8FATReadBuffer);     // Write Buffer to Sector
    
        /* Check Sector Size */
        if(FAThandle->WHandler.SectorIndex == FAThandle->u16FAT_Sector_Size)
        {
            FAThandle->WHandler.SectorIndex=0;
            FAThandle->WHandler.ClusterIndex++;    
            u8ChangeSector=1;
        }
    
        /* Check Cluster Size */
        if(FAThandle->WHandler.ClusterIndex == FAThandle->u16FAT_Cluster_Size)
        {
            FAThandle->WHandler.ClusterIndex=0;
            u16TempFat=FAT_SearchAvailableFAT(FAThandle,u8FATReadBuffer,FAThandle->WHandler.CurrentFatEntry);   
            (void)FAT_Entry(FAThandle,u8FATReadBuffer,FAThandle->WHandler.CurrentFatEntry,u16TempFat,WRITE_ENTRY);
            FAThandle->WHandler.CurrentFatEntry=u16TempFat;
            u8ChangeSector=1;
        }
    }
}
/***************************************************************************************/
UINT16 
FAT_FileRead(FATHandler *FAThandle,UINT8 *pu8UserBuffer)
{
    UINT32 u32SectorToRead; 
    UINT16 u16BufferSize;
    static UINT8 flag_next_entry = FALSE;

    if(FAThandle->RHandler.File_Size==0)
        return(0);   
    
    /*change by b06862*/
    if( flag_next_entry == TRUE )
    {
        FAThandle->RHandler.SectorOffset=0;
        FAThandle->RHandler.FAT_Entry = FAT_Entry(FAThandle,pu8UserBuffer,FAThandle->RHandler.FAT_Entry,0,NEXT_ENTRY); // Get Next FAT Entry
        flag_next_entry = FALSE;
    }
    
    u32SectorToRead= FAThandle->u16FAT_Data_BASE + ((FAThandle->RHandler.FAT_Entry-2)*FAThandle->u16FAT_Cluster_Size) + FAThandle->RHandler.SectorOffset;
    
    GetPhysicalBlock(u32SectorToRead,pu8UserBuffer);

    if(FAThandle->RHandler.File_Size > FAThandle->u16FAT_Sector_Size)
    {
        FAThandle->RHandler.File_Size-=FAThandle->u16FAT_Sector_Size;
        u16BufferSize=512;
    }
    else
    {
        u16BufferSize=(UINT16)FAThandle->RHandler.File_Size;
        FAThandle->RHandler.File_Size=0;
    }
    
    if(FAThandle->RHandler.SectorOffset < (FAThandle->u16FAT_Cluster_Size)-1)
        FAThandle->RHandler.SectorOffset++;        
    else/*change by b06862*/
    {
        //FAThandle->RHandler.SectorOffset=0;
        //FAThandle->RHandler.FAT_Entry = FAT_Entry(FAThandle,pu8UserBuffer,FAThandle->RHandler.FAT_Entry,0,NEXT_ENTRY); // Get Next FAT Entry
        flag_next_entry = TRUE;
    }
        
    return(u16BufferSize);    
}



/***************************************************************************************/
void 
FAT_FileNameOrganizer(UINT8 *pu8FileName,UINT8 *pu8Destiny)
{
    UINT8 u8Counter=0;    
    
    while(u8Counter<12)
    {
        if(*pu8FileName != '.')
            *pu8Destiny++=*pu8FileName++;
        else
        {
            if(u8Counter<8)
                *pu8Destiny++=0x20;
            else
                pu8FileName++;    
        }
        u8Counter++;
    }
}

/***************************************************************************************/
UINT8 
FAT_FileDelete(FATHandler *FAThandle, UINT8 *u8FATReadBuffer, UINT8 *pu8FileName)
{
    UINT8  u8FileName[11];
    UINT8  u8ErrorCode=ERROR_IDLE;
    UINT8  u8Flag=FALSE;
    UINT8  u8Counter=0;
    UINT16 u16Block=0;
    UINT16 u16Index=0;
    UINT16 u16BlockNum=FAThandle->u16FAT_Data_BASE-FAThandle->u16FAT_Root_BASE;
    root_Entries *sFileStructure;                                   


    FAT_FileNameOrganizer(pu8FileName,u8FileName);
    
    while(u16Block < u16BlockNum && u8ErrorCode==ERROR_IDLE)
    {
    
        GetPhysicalBlock(FAThandle->u16FAT_Root_BASE+u16Block,u8FATReadBuffer);
        sFileStructure = (root_Entries*)u8FATReadBuffer;

        while(u16Index<FAThandle->u16FAT_Sector_Size && u8ErrorCode==ERROR_IDLE)    
        {
            if(sFileStructure->FileName[0]==FILE_Clear)     // Directory empty condition
                return(FILE_NOT_FOUND);
            
            if(sFileStructure->FileName[0] == u8FileName[0])
            {
                u8Flag=TRUE;
                u8Counter=0;
                while(u8Flag==TRUE && u8Counter < 10)
                {
                    u8Counter++;
                     if(sFileStructure->FileName[u8Counter] != u8FileName[u8Counter])
                         u8Flag=FALSE;    
                }
            }
            if(u8Flag==TRUE)
            {
                // Mark 1st Name Entry as deleted
                sFileStructure->FileName[0]=FILE_Erased;
                StorePhysicalBLock(FAThandle->u16FAT_Root_BASE+u16Block,u8FATReadBuffer);                    
                return(FILE_DELETED);
            }
            u16Index+=RootEntrySize;
            sFileStructure++;
        }
        u16Block++;
        u16Index=0;
    }
    return(FILE_NOT_FOUND);
}

/***************************************************************************************/
UINT8 
FAT_FileOpen(FATHandler *FAThandle,UINT8 *u8FATReadBuffer,UINT8 *pu8FileName,UINT8 u8Function)
{
    
    UINT16 u16Temporal;
    UINT8  u8FileName[11];
    UINT8  u8Counter=0;
    UINT8  u8Flag=FALSE;
    UINT16 u16Index;
    UINT16 u16Block;
    UINT16 u16BlockNum=FAThandle->u16FAT_Data_BASE-FAThandle->u16FAT_Root_BASE;
    UINT8  u8ErrorCode=ERROR_IDLE;
    UINT8  *pu8Pointer;
    root_Entries *sFileStructure;                                   
    
    FAT_FileNameOrganizer(pu8FileName,&u8FileName[0]);
    
    u16Block=0;
    
    while(u16Block < u16BlockNum && u8ErrorCode==ERROR_IDLE)
    {
    
        GetPhysicalBlock(FAThandle->u16FAT_Root_BASE+u16Block,u8FATReadBuffer);
        sFileStructure = (root_Entries*)u8FATReadBuffer;

        u16Index=0;
        while(u16Index<FAThandle->u16FAT_Sector_Size && u8ErrorCode==ERROR_IDLE)    
        {
            /* If Read or Modify Function */
            if(u8Function==READ || u8Function==MODIFY)
            {
                if(sFileStructure->FileName[0]==FILE_Clear) 
                    u8ErrorCode=FILE_NOT_FOUND;
        
                if(sFileStructure->FileName[0] == u8FileName[0])
                {
                    u8Flag=TRUE;
                    u8Counter=0;
                    while(u8Flag==TRUE && u8Counter < 10)
                    {
                        u8Counter++;
                        if(sFileStructure->FileName[u8Counter] != u8FileName[u8Counter])
                            u8Flag=FALSE;    
                    }
                    if(u8Flag==TRUE)
                    {
                        /* If Read Function */
                        if(u8Function==READ)
                        {
                            FAThandle->RHandler.Dir_Entry=(u16Block*RootEntrySize)+((u16Index)/RootEntrySize);
                            FAThandle->RHandler.File_Size=LWordSwap(sFileStructure->SizeofFile);
                            FAThandle->RHandler.FAT_Entry=ByteSwap(sFileStructure->ClusterNumber);
                            FAThandle->RHandler.SectorOffset=0;
                            u8ErrorCode=FILE_FOUND;
                        } 
                        /* If Modify Function */
                        else
                        {
                            pu8Pointer=FAThandle->WHandler.FileName;
                            for(u8Counter=0;u8Counter<11;u8Counter++)
                                *pu8Pointer++=u8FileName[u8Counter];
                            FAThandle->WHandler.Dir_Entry=(u16Block*RootEntrySize)+((u16Index)/RootEntrySize);
                            FAThandle->WHandler.File_Size=LWordSwap(sFileStructure->SizeofFile);
                            FAThandle->WHandler.BaseFatEntry=ByteSwap(sFileStructure->ClusterNumber);
                            
                            if(FAThandle->WHandler.BaseFatEntry != 0)
                            {
                                u16Temporal=FAThandle->WHandler.BaseFatEntry;
                                do
                                {
                                    FAThandle->WHandler.CurrentFatEntry=FAThandle->WHandler.BaseFatEntry;
                                    FAThandle->WHandler.BaseFatEntry=FAT_Entry(FAThandle,u8FATReadBuffer,FAThandle->WHandler.CurrentFatEntry,0,NEXT_ENTRY);
                                }while(FAThandle->WHandler.BaseFatEntry!=0xFFFF);
                                FAThandle->WHandler.BaseFatEntry=u16Temporal;
                            } 
                            else
                            {
                                FAThandle->WHandler.BaseFatEntry=FAT_SearchAvailableFAT(FAThandle,u8FATReadBuffer,0);
                                FAThandle->WHandler.CurrentFatEntry=FAThandle->WHandler.BaseFatEntry;
                            }

                            /***/
                            u8Counter=0;
                            u8ErrorCode=(UINT8)FAThandle->u16FAT_Cluster_Size;
                            while(u8ErrorCode != 0x01)
                            {
                                u8Counter++;
                                u8ErrorCode=u8ErrorCode>>1;
                            }
                            /***/
                            
                            u16Temporal=(UINT16)FAThandle->WHandler.File_Size % (FAThandle->u16FAT_Sector_Size<<4);
                            FAThandle->WHandler.ClusterIndex= u16Temporal/FAThandle->u16FAT_Sector_Size;
                            FAThandle->WHandler.SectorIndex=  u16Temporal%FAThandle->u16FAT_Sector_Size;
                            u8ErrorCode=FILE_FOUND;
                        }
                    }
                }
            }

            /* If Write function */
            if(u8Function==CREATE)
            {
                if(sFileStructure->FileName[0]==FILE_Clear || sFileStructure->FileName[0]==FILE_Erased) 
                {
                    
                    pu8Pointer=FAThandle->WHandler.FileName;
                    for(u8Counter=0;u8Counter<11;u8Counter++)
                        *pu8Pointer++=u8FileName[u8Counter];

                    FAThandle->WHandler.Dir_Entry=(u16Block*RootEntrySize)+((u16Index)/RootEntrySize);
                    FAThandle->WHandler.File_Size=0;
                    FAThandle->WHandler.BaseFatEntry=FAT_SearchAvailableFAT(FAThandle,u8FATReadBuffer,0);
                    FAThandle->WHandler.CurrentFatEntry=FAThandle->WHandler.BaseFatEntry;
                    FAThandle->WHandler.ClusterIndex=0;
                    FAThandle->WHandler.SectorIndex=0;
        
                    if(FAThandle->WHandler.BaseFatEntry)
                        u8ErrorCode=FILE_CREATE_OK;
                    else
                        u8ErrorCode=NO_FAT_ENTRY_AVAIlABLE;
                }
            }
            sFileStructure++;
            u16Index+=RootEntrySize;
        }
        u16Block++;
    }
    if(u16BlockNum==u16Block)
        u8ErrorCode=NO_FILE_ENTRY_AVAILABLE;
    
    return(u8ErrorCode);
}