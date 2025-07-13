# auto_integrate_v2.py - Try UTF-8 encoding for auto-integration
import os
import shutil

def safe_read_file(filename):
    """Safely read file with multiple encoding attempts"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"✅ Successfully read {filename} with {encoding} encoding")
            return content, encoding
        except UnicodeDecodeError:
            continue
    
    raise Exception("Could not read file with any encoding")

def auto_integrate_smart_detection():
    """Attempt automatic integration with better encoding handling"""
    
    try:
        # Read main.py safely
        content, encoding = safe_read_file('main.py')
        print(f"📄 Read main.py successfully")
        
        # Backup
        shutil.copy('main.py', 'main_backup_v2.py')
        print("✅ Created backup: main_backup_v2.py")
        
        # Step 1: Add import
        import_line = "\n# ✅ SMART INTENT DETECTION - Advanced AI-powered context awareness\nfrom smart_context_detection import SmartIntentDetector\n"
        
        if 'import threading' in content:
            content = content.replace('import threading', 'import threading' + import_line)
            print("✅ Added smart detection import")
        
        # Step 2: Add detector initialization
        detector_init = "\n# ✅ Initialize smart intent detector\nsmart_detector = SmartIntentDetector()\nprint('[Buddy V2] 🧠 Smart intent detection system loaded')\n"
        
        if 'state_lock = threading.Lock()' in content:
            content = content.replace('state_lock = threading.Lock()', 'state_lock = threading.Lock()' + detector_init)
            print("✅ Added detector initialization")
        
        # Step 3: Add smart handler function
        smart_handler = '''
def handle_smart_intent_detection(text, audio_data):
    """
    🧠 SMART: Use AI-powered intent detection instead of simple pattern matching
    Returns True if handled directly, False if should go to conversation
    """
    global current_user
    
    # Analyze the user's intent with advanced reasoning
    analysis = smart_detector.analyze_intent(text)
    
    print(f"[SmartIntent] 🧠 Analysis: {analysis['primary_intent']} (confidence: {analysis['confidence']:.2f})")
    if analysis['reasoning']:
        print(f"[SmartIntent] 💭 Reasoning: {', '.join(analysis['reasoning'])}")
    
    if analysis['exclusion_flags']:
        print(f"[SmartIntent] 🚫 Exclusions: {', '.join(analysis['exclusion_flags'])}")
    
    # Only respond directly if high confidence and no exclusions
    if analysis['should_respond_directly']:
        
        if analysis['primary_intent'] == 'TIME_REQUEST':
            print(f"[SmartIntent] 🕐 SMART TIME RESPONSE for: '{text}'")
            brisbane_time = get_current_brisbane_time()
            if IS_SUNSHINE_COAST:
                speak_async(f"It's {brisbane_time['time_12h']} here in Birtinya, Sunshine Coast.", DEFAULT_LANG)
            else:
                speak_async(f"It's {brisbane_time['time_12h']} here in {USER_PRECISE_LOCATION}.", DEFAULT_LANG)
            return True
            
        elif analysis['primary_intent'] == 'DATE_REQUEST':
            print(f"[SmartIntent] 📅 SMART DATE RESPONSE for: '{text}'")
            brisbane_time = get_current_brisbane_time()
            speak_async(f"Today is {brisbane_time['date']}.", DEFAULT_LANG)
            return True
            
        elif analysis['primary_intent'] == 'LOCATION_REQUEST':
            print(f"[SmartIntent] 📍 SMART LOCATION RESPONSE for: '{text}'")
            if IS_SUNSHINE_COAST:
                speak_async(f"I'm located in Birtinya, Sunshine Coast, Queensland {USER_POSTCODE_PRECISE}. Near USC and Stockland Birtinya.", DEFAULT_LANG)
            else:
                speak_async(f"I'm located in {USER_PRECISE_LOCATION} {USER_POSTCODE_PRECISE}.", DEFAULT_LANG)
            return True
    
    # If not a direct response, let it go to normal conversation
    print(f"[SmartIntent] 💬 CONVERSATION MODE for: '{text}' - Will use LLaMA")
    return False

'''
        
        if 'def handle_full_duplex_conversation():' in content:
            content = content.replace('def handle_full_duplex_conversation():', smart_handler + '\ndef handle_full_duplex_conversation():')
            print("✅ Added smart handler function")
        
        # Step 4: Replace old detection logic (simplified approach)
        # Look for the time question pattern and replace the whole block
        if 'if is_time_question(text):' in content:
            # Find the block and replace it
            lines = content.split('\n')
            new_lines = []
            skip_mode = False
            
            for line in lines:
                if 'if is_time_question(text):' in line:
                    # Start of old detection block
                    new_lines.append('                # 🧠 SMART INTENT DETECTION - AI-powered context awareness')
                    new_lines.append('                if handle_smart_intent_detection(text, audio_data):')
                    new_lines.append('                    continue  # Direct response was given, continue to next iteration')
                    skip_mode = True
                    continue
                elif skip_mode and 'continue' in line and 'date' in lines[max(0, len(new_lines)-10):len(new_lines)]:
                    # End of old detection block (found the last continue)
                    skip_mode = False
                    continue
                elif not skip_mode:
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
            print("✅ Replaced old detection logic with smart detection")
        
        # Save the updated file
        with open('main.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("🎉 AUTO-INTEGRATION SUCCESSFUL!")
        print("🚀 Now run: python main.py")
        return True
        
    except Exception as e:
        print(f"❌ Auto-integration failed: {e}")
        print("📝 Use the manual integration steps instead")
        return False

if __name__ == "__main__":
    print("🚀 ATTEMPTING AUTO-INTEGRATION V2")
    print("Current Time: 2025-07-06 05:55:30 UTC (3:55 PM Brisbane)")
    print()
    
    if auto_integrate_smart_detection():
        print("\n✅ SUCCESS! Buddy is now smart and context-aware!")
        print("Test with:")
        print("🗣️ 'I had a bad day' → Should have conversation")
        print("🗣️ 'What time is it?' → Should give time")
        print("🗣️ 'How was your day?' → Should ask about experiences")
    else:
        print("\n📋 Use manual integration instead")