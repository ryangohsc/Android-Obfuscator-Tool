# ICT-2207-A2

Key files/directories to note
```
.
├── dumpster/  .  .  .  .  # Working directory for all APK related files (extraction)
│
├── modules/  .  .  .  .   # All python logic
│       │
│       └── obfuscator.py  # Trigger point for obfuscation functions
│
├── SAMPLE_FILES/
├── static/
│   │
│   ├── css/
│   ├── html/
│   ├── js/
│   │   │
│   │   └── userScripts.js # Handles UI/Logic communication
│   │
│   └── tmp/  .  .  .  .   # Working directory for generated HTML/txt files
│
├── templates/
│       │
│       └── index.html  .  # Main UI
│
├── tools/  .  .  .  .  .  # Miscellaneous tools
│
└── main.py  .  .  .  .    # Main launch point and routes
```

## Setup
1. **Install prereqs**

   ```
   pip3 install -r requirements.txt
   ```


2. **Run**

   ```
   python3 main.py
   ```
