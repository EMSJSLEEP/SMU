#!/bin/bash

CYG_MODULE_DRIVER_PATH_PREFIX="/mix/driver/cyg/"
CYG_COMMON_DRIVER_PATH_PREFIX="/mix/driver/cyg/common/"

copy_module_driver_to_mix()
{
  dir=${PWD##*/}
  echo "$dir"
  module_folder=${dir,,}
  echo "$module_folder"
  target_folder_name=$CYG_MODULE_DRIVER_PATH_PREFIX$module_folder
  if [ -d "$target_folder_name" ]; then
	  rm -rf $target_folder_name
  fi
  if [ -d "driver" ]; then
	  echo "driver folder exists."
  else
	  echo "No driver folder exists"
	  exit 1
  fi
  mkdir -p $target_folder_name/
  cp -r driver/module $target_folder_name/
  echo "Success copy dirver folder to $target_folder_name"
}

copy_common_driver_to_mix()
{
  # search the ic ipcore module bus and so on folder 
  # copy these folders' content into /tmp/mix/driver/cyg/common/
  if [ -d "ic" ]; then
	 cp -rf ic/* $CYG_COMMON_DRIVER_PATH_PREFIX"ic"/
  elif [ -d "bus" ]; then
	 cp -rf bus/* $CYG_COMMON_DRIVER_PATH_PREFIX"bus"/
  elif [ -d "ipcore" ]; then
	 cp -rf ipcore/* $CYG_COMMON_DRIVER_PATH_PREFIX"ipcore"/
  elif [ -d "module" ]; then
	 cp -rf module/* $CYG_COMMON_DRIVER_PATH_PREFIX"module"/
  fi 
}


copy_ip_driver_to_mix()
{
  if [ -d "ip" ] || [ -d "driver/ipcore" ]; then
	  cp -rf driver/ipcore/* $CYG_COMMON_DRIVER_PATH_PREFIX"ipcore"/
  else
	  echo "This is not a IP driver"
	  exit 1
  fi
}


copy_py_to_mix()
{
  if [ -d "ip" ] || [ -d "driver/ipcore" ]; then
	copy_ip_driver_to_mix
  elif [ -d "ic" ] && [ -d "ipcore" ]; then
	copy_common_driver_to_mix
  elif [ -d "driver" ] && [ ! -d "ip" ]; then
        copy_module_driver_to_mix
  else
      echo "Invald driver folder."
      exit 1
  fi

}

copy_py_to_mix
