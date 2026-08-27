# External Sources

Keep external repositories and copied code separate from project code. Do not clone external repositories into this directory yet.

During baseline analysis and original-condition reproduction, treat upstream repositories as read-only references. Do not modify their code, notebooks, configuration, requirements, README, datasets, or weights.

After baseline reproduction is complete, modifications may be considered during project integration only when the verified license permits modification and redistribution. Even then, prefer a wrapper, adapter, or independent implementation in this repository over changing upstream directly.

For every source used, record its original URL, commit or tag, license, purpose, referenced files, and any changes made. If integration changes are made, also record the modified files and a precise description of each change. Preserve attribution and comply with the source license. If external code is later used, consider a submodule or another traceable integration method rather than copying it into `src/` without attribution.

TODO: Add verified source records after a baseline repository or dataset is selected.