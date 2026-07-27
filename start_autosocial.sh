#!/bin/bash
set -e

# Instagram Gradient Colors (TrueColor)
C1='\033[38;2;252;175;69m'
C2='\033[38;2;247;119;55m'
C3='\033[38;2;245;96;64m'
C4='\033[38;2;225;48;108m'
C5='\033[38;2;193;53;132m'
C6='\033[38;2;131;58;180m'
NC='\033[0m' # No Color
GREEN='\033[0;32m'
GRAY='\033[1;30m'

echo -e ""
echo -e "${C1}    ___         __        _____            _       __ ${NC}"
echo -e "${C2}   /   | __  __/ /_____  / ___/____  _____(_)___ _/ / ${NC}"
echo -e "${C3}  / /| |/ / / / __/ __ \ \__ \/ __ \/ ___/ / __ \`/ /  ${NC}"
echo -e "${C4} / ___ / /_/ / /_/ /_/ /___/ / /_/ / /__/ / /_/ / /   ${NC}"
echo -e "${C5}/_/  |_\__,_/\__/\____//____/\____/\___/_/\__,_/_/    ${NC}"
echo -e "${C6}                                                      ${NC}"
echo -e "       ${C4}✨ AI-Powered Instagram Automator ✨${NC}\n"

echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${C1}[1/3]${NC} Environment & API Verification..."
if [ ! -f .env ]; then
    echo -e "❌ Error: .env file not found!"
    exit 1
fi
export PYTHONPATH=src
python check_providers.py
echo -e "${GREEN}✓ Systems verified and active.${NC}\n"

echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${C3}[2/3]${NC} Starting AI Generation Engine...\n"
python run_real.py

echo -e "\n${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${C5}[3/3]${NC} Workflow Complete!"
echo -e "Check your Instagram feed to see your newly generated post!"
echo -e "${C6}--- AutoSocial AI Shutdown Safely ---${NC}\n"
