# Remotely Access the Raspberry Pi via Tailscale

We are using [Tailscale](https://tailscale.com) to remotely access and manage the I-STEM Raspberry Pi (`cvpi`) from anywhere. This enables SSH access over a secure private network without needing port forwarding or public IPs.

This guide walks you through how to get connected to the Pi using Tailscale.


## Step 1: Create a Tailscale Account

Go to [login.tailscale.com](https://login.tailscale.com) and create an account.

<img src="screenshot1.png" alt="screenshot1" width="250"/>


## Step 2: Follow the Prompts to Install Tailscale and Add Your First Device

Download and install Tailscale from [tailscale.com/download](https://tailscale.com/download) on the device you'll be using to access the Pi.

<img src="screenshot2.png" alt="screenshot1" width="500"/>

Your device should appear on the screen like this once connected.


## Step 3: Skip the Rest of the Introduction

<img src="screenshot3.png" alt="screenshot1" width="500"/>

Tailscale will prompt you to add a second device. Scroll to the bottom of the page and click “Skip this introduction →”.


## Step 4: Accept Invite for `cvpi`

[https://login.tailscale.com/admin/invite/EVwhLLnNzaT5xVJgjgTy11](https://login.tailscale.com/admin/invite/EVwhLLnNzaT5xVJgjgTy11)

<img src="screenshot4.png" alt="screenshot4" width="250"/>

Navigate to the invite link and click **“Accept invite”**.

Once accepted, you should see both your machine and `cvpi` listed in your Tailnet.


## Step 5: Test Your Connection

Test your connection with the following commands.

```bash
$ tailscale status
```

```bash
$ ping cvpi.tail9442c1.ts.net
```

If `tailscale status` does not show `cvpi` or `cvpi` does not resolve, ensure that Tailscale is running and `cvpi` was correctly added to your Tailnet.


## Step 6: SSH into `cvpi`

You can now SSH into the Raspberry Pi using the following command. The password is ('water').

```bash
$ ssh stem@cvpi.tail9442c1.ts.net
```


## Summary

- You now have secure SSH access to the I-STEM Raspberry Pi via Tailscale.
- Always use the full hostname `cvpi.tail9442c1.ts.net` when connecting.
- Make sure Tailscale is running on your device before attempting to SSH.
- Use `ssh stem@cvpi.tail9442c1.ts.net` to access the Pi while it’s online.
- You can use tools like VS Code Remote SSH or SCP to develop and transfer files.

Need help? Reach out to Owen.

### Special Thanks

Huge thanks to [**Aahil Lakhani**](https://github.com/Aahil52) for helping me understand Tailscale and guiding me through the setup process.
