from imapclient import IMAPClient
import ssl

def get_mailbox_storage_percent(email, password):
    context = ssl.create_default_context()

    with IMAPClient(host='i.mail25.info', port=993, ssl=True, ssl_context=context) as client:
        client.login(email, password)

        total_used_bytes = 0

        # 🔄 Step 1: Loop through all folders and sum their SIZE
        folders = client.list_folders()
        for flags, delimiter, folder_name in folders:
            try:
                client.select_folder(folder_name, readonly=True)
                status = client.folder_status(folder_name, ['SIZE'])
                folder_size = status.get(b'SIZE', 0)
                total_used_bytes += folder_size
            except Exception as e:
                print(f"⚠️ Could not read folder {folder_name.decode('utf-8', 'ignore')}: {e}")

        # 🧠 Step 2: Try to get the quota using get_quota or get_quota_root
        quota_limit = None
        try:
            # First try get_quota_root which may give more reliable info
            quota_root = client.get_quota_root('INBOX')
            if isinstance(quota_root, list):
                for entry in quota_root:
                    if len(entry) >= 2 and isinstance(entry[1], list):
                        for quota_info in entry[1]:
                            if quota_info[0] == b'STORAGE':
                                quota_limit = quota_info[2] * 1024  # From KB to bytes
                                break
        except Exception as e:
            print(f"⚠️ Could not fetch quota root for {email}: {e}")

        # Step 3: If quota is still None, fallback to default (500 MB)
        if quota_limit is None:
            quota_limit = 500 * 1024 * 1024

        percent = (total_used_bytes / quota_limit) * 100

        print(f"[{email}] Total mailbox usage: {total_used_bytes / (1024*1024):.2f} MB of {quota_limit / (1024*1024):.2f} MB")
        print(f"{email} is at {percent:.2f}% of quota")

        return percent


def get_email_metadata(email, password, max_per_folder=20):
    import email as em
    context = ssl.create_default_context()
    metadata = {}

    with IMAPClient(host='i.mail25.info', port=993, ssl=True, ssl_context=context) as client:
        client.login(email, password)

        # Get list of available folders
        available_folders = [folder_name for _, _, folder_name in client.list_folders()]
        desired_folders = ['INBOX', 'Sent', 'Spam', 'Junk', 'Trash']
        folders_to_check = [f for f in desired_folders if f in available_folders]

        # Optionally print missing folders
        missing = set(desired_folders) - set(folders_to_check)
        for folder in missing:
            print(f"⚠️ Skipping missing folder: {folder} for {email}")

        for folder in folders_to_check:
            try:
                client.select_folder(folder, readonly=True)
                messages = client.search('ALL')
                messages = messages[-max_per_folder:]  # get last N emails

                response = client.fetch(messages, ['ENVELOPE'])

                folder_data = []
                for msgid, data in response.items():
                    envelope = data[b'ENVELOPE']
                    subject = envelope.subject.decode('utf-8', errors='ignore') if envelope.subject else ""
                    from_addr = envelope.from_[0] if envelope.from_ else None
                    sender_email = f"{from_addr.mailbox.decode()}@{from_addr.host.decode()}" if from_addr else ""
                    folder_data.append({'from': sender_email, 'subject': subject})

                metadata[folder] = folder_data

            except Exception as e:
                print(f"⚠️ Failed to extract metadata from {folder} for {email}: {e}")

    return metadata
