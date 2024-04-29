@echo off

rem When running the python file, if the files has _test.py we
REM treat it as a test file and run it with pytest. Otherwise
REM we run it with regular python.

REM To figure out if the file has _test.py or not, we
REM use findstr with case insentivity (/i) and checking
REM the end of the string (/e). If a match is found ERRORLEVEL
REM is set to 0. So in the if statement if errorlevel is 1 or higher,
REM we treat this as a regular python file. Otherwise, ERRORLEVEL
REM must be 0 and we treat it as a test file and run it with pytest.

REM See the following stackoverflow page for more details:
REM https://stackoverflow.com/questions/7005951/batch-file-find-if-substring-is-in-string-not-in-a-file


::set file_path=%1
::set file_path_without_test_py=%file_path:_test.py=%

::IF %file_path% == %file_path_without_test_py% (
::%DELIBERATE_PRACTICE_CONDA_DIR%\python.exe %1
::) ELSE (
::%DELIBERATE_PRACTICE_CONDA_DIR%\Scripts\pytest.exe %1
::) 

::set file_path=%1
::set file_path_without_test_py=%file_path:_test.py=%
echo:%1| findstr /c:"_test.py" /i /e 1>nul

IF ERRORLEVEL 1 (
%DELIBERATE_PRACTICE_CONDA_DIR%\python.exe %1
) ELSE (
%DELIBERATE_PRACTICE_CONDA_DIR%\Scripts\pytest.exe %1
) 