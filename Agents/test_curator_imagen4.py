# test_curator_imagen4.py
from agents.curator_agent import CuratorAgent

if __name__ == "__main__":
    agent = CuratorAgent()
    input_image = "image.png"

    print("🔍 Step 1: Generating mask...")
    try:
        mask = agent.create_mask(input_image)
        mask.save("mask_debug.png")
        print("✅ mask_debug.png saved! (Check: product should be BLACK)")
    except Exception as e:
        print(f"❌ Mask failed: {str(e)}")
        exit()

    print("\n🖼️  Step 2: Creating studio enhancement...")
    try:
        studio = agent.create_studio_shot(input_image)
        # Handle different ways the result might be returned
        if hasattr(studio, 'save'):
            studio.save("studio_vase_4k.png")
            print("✅ Studio image saved as PIL Image")
        else:
            # If it's a VertexImage, convert to PIL and save
            with open("studio_vase_4k.png", "wb") as f:
                f.write(studio._image_bytes)
            print("✅ Studio image saved as VertexImage")
    except Exception as e:
        print(f"❌ Studio shot failed: {str(e)}")
        print(f"💡 Error type: {type(e).__name__}")
        import traceback
        print(f"🔍 Full traceback: {traceback.format_exc()}")
        exit()

    print("\n🏡 Step 3: Creating lifestyle mockup...")
    try:
        lifestyle = agent.create_lifestyle_mockup(input_image)
        # Handle different ways the result might be returned
        if hasattr(lifestyle, 'save'):
            lifestyle.save("lifestyle_vase_4k.png")
            print("✅ Lifestyle image saved as PIL Image")
        else:
            # If it's a VertexImage, convert to PIL and save
            with open("lifestyle_vase_4k.png", "wb") as f:
                f.write(lifestyle._image_bytes)
            print("✅ Lifestyle image saved as VertexImage")
    except Exception as e:
        print(f"❌ Lifestyle mockup failed: {str(e)}")
        exit()

    print("\n🎉 SUCCESS! Your Curator Agent is NOW WORKING with Imagen 4.0 Ultra!")