# Linux Kernel Security and Backport Suite

This repo documents the process of patch applying from the upstream kernel development tree to LTS/ELS kernels in case of bugs and vulnerabilities.

## Tree:
- `patches/`: generated through `git format-patch`.
- `validate_backport.sh`: Simple script that runs the official linux kernel's `checkpatch.pl`.
- `packaging`: RPM `kernel.spec`.

## How does that work
1. Find the upstream correction commit
```bash
git format-patch -1 <commit-hash> -o ./patches/
```
2. Apply it
```bash
git am -3 ./patches/0001-*.patch
```
If any conflict, investigate it and do the proper adaptations 
3. Validate it:
```bash
./validate_backport.sh
```
## Real test: powerpc/irq
* Curiosity: IRQ means Interruption ReQuest. I know it because I'm currently doing my own kernel. Well, I don't know how it happens in PowerPC, but at least in AMD64 you have the IDT (Interrupt Descriptor Table), and there's a section of interrupts for IRQ's, basically.   
    Searching more, I found out that you can do:
    ```bash
    cat /proc/interrupts
    ```
    It'll show how many times each IRQ triggered an interrupt. To do it, it needs arch_show_interrupts() function (arch is basically for architecture dependent things. Yeah, you learn a lot doing a kernel). Basically, a guy used the function irq_proc_emit_counts() in it (which is inside kernel/irq/proc.c). The problem: in embedded systems, you can compile it without /proc (CONFIG_PROC_FS=n). So, naturally it wasn't compiling.
    The patch was simple: just add
    ```c
    #ifdef CONFIG_PROC_FS
    ```
(I really love C preprocessor)

So, I applied the patch `patches/0001-powerpc-irq-Fix-build-with-CONFIG_PROC_FS-n.patch` to test this situation.

## Real CVE test: CVE-2024-41059 (fs/hfsplus)
* Context: HFS+ means Hierarchical File System Plus, also known as Mac OS Extended: an Apple filesystem used until 2017. So, inside fs/hfsplus/xattr.c file (eXtended ATTRibutes, system file metadata), the hfsplus_listxattr was using kmalloc to allocate memory and keeping it under strbuf variable. So Syzbot KMSAN detected an uninitialized memory read (`uninit-value in sized_strscpy`) in `copy_name` (`fs/hfsplus/xattr.c`). Basically, `strbuf` was allocated with `kmalloc()`, which means it wasn't zeroed: information disclosure. `kmalloc()` was replaced by `kzalloc()` and the patch was applied against Linux 5.15 LTS.

## Packaging:
Just do:
```bash
rpmbuild -ba packaging/rpm/kernel.spec
```
or
```
make bindeb-pkg -j$(nproc)
```
