using UnityEngine;
using UnityEditor;

/// <summary>
/// Universal custom ShaderGUI interface, automatic processing of Shader Alpha Blend, Alpha Test macro settings
/// </summary>
public class CustomShaderGUI : ShaderGUI
{
    public enum BlendMode
    {
        Opaque,
        Cutout,
        Fade,   // Old school alpha-blending mode, fresnel does not affect amount of transparency
        Transparent // Physically plausible transparency mode, implemented as alpha pre-multiply
    }

    public static readonly string[] blendNames = System.Enum.GetNames(typeof(BlendMode));

    protected MaterialEditor currentMaterialEditor = null;
    protected Material currentMaterial = null;
    protected Shader currentShader = null;
    protected MaterialProperty[] currentProps = null;
    private const string shaderEffectControlPropertyName = "MaterialEffect";
    private const string shaderEffectKeyWord = "_Effect";
    private string[] shaderEffects = { "_Effect_Dissolve", "_Effect_Emission" };
    private static bool showKeyword = false;
    private static bool showDebugGUI = false;

    public override void OnGUI(MaterialEditor materialEditor, MaterialProperty[] props)
    {
        currentMaterial = materialEditor.target as Material;
        currentMaterialEditor = materialEditor;
        currentProps = props;
        currentShader = currentMaterial.shader;

        for (int i = 0; i < ShaderUtil.GetPropertyCount(currentShader); i++)
        {
            var description = ShaderUtil.GetPropertyDescription(currentShader, i);
            var name = ShaderUtil.GetPropertyName(currentShader, i);
            var property = FindProperty(name, props);
            ShowShaderProperty(name, description, property);
        }
        showDebugGUI = GUILayout.Toggle(showDebugGUI, "Show Debug Info");
        if (showDebugGUI)
        {
            CustomShadingDebugger.ShowShaderDebugParam();
            ShowShaderKeyword();
        }
        materialEditor.RenderQueueField();
    }

    public virtual void ShowShaderProperty(string name, string description, MaterialProperty property)
    {
        if (ShowBlendShaderProperty(name, description, property))
            return;
        else if (HandleCommonProperty(name, description, property))
            return;
        else if (ShowCustomShaderProperty(name, description, property))
            return;
        HandleProperty(name, description, property);
    }

    public virtual bool ShowBlendShaderProperty(string name, string description, MaterialProperty property)
    {
        if (description == "BlendMode")
        {
            var minBlendMode = BlendMode.Opaque;
            var maxBlendMode = BlendMode.Transparent;
            if (currentShader.name == "CYShaders/NextGenCustomShadingCloth")
                maxBlendMode = BlendMode.Cutout;
            else if (currentShader.name == "CYShaders/NextGenCustomShadingCloth_Transparent")
                minBlendMode = BlendMode.Fade;
            ShowBlendMode(property, minBlendMode, maxBlendMode);
            return true;
        }
        else if (description.StartsWith("__"))
            return true;
        else if (!IsSpecificProperty("_Mode", 1) && name == "_Cutoff")
            return true;
        return false;
    }

    public virtual bool ShowCustomShaderProperty(string name, string description, MaterialProperty property)
    {
        //Multi-material mask distinction
        if (IsSpecificProperty("CHANNELMODE", 0) && name == "NDF_SECOND")
            return true;
        //Skin
        if (!IsSpecificProperty("DIFFUSE_TYPE", 3) && (name.StartsWith("_Skin")))
            return true;
        //
        if (!(IsSpecificProperty("NDF", 1) || IsSpecificProperty("NDF", 2)) && name == "_Anisotropic")
            return true;
        //Stockings
        if (!IsSpecificProperty("SPECIAL_MAT", 1) && name.StartsWith("_Stocking"))
            return true;
        //matcap
        if (!IsSpecificProperty("SPECIAL_MAT", 2) && name.StartsWith("_Matcap"))
            return true;
        //Hair effect
        if (!IsSpecificProperty("SPECIAL_MAT", 3) && name.StartsWith("_Hair"))
            return true;

        return false;
    }

    public bool HandleCommonProperty(string name, string description, MaterialProperty property)
    {
        //Custom reflector
        //if (!IsSpecificProperty("CUSTOM_REFLECTIONPROBE", 1) && name.StartsWith("_CustomReflectionProbe"))
        //    return true;
        //天气
        if (!Shader.IsKeywordEnabled("RAIN_EFFECT") && name.StartsWith("_Rain"))
            return true;
        if (name == "_RainEffectParams")
        {
            ShowRainEffectParam(property);
            return true;
        }
        if (name == "_IndirectLightControl")
        {
            ShowIndirectLightingParam(property);
            return true;
        }
        if(name == "_RimLightingControl")
        {
            ShowRimLightingParam(property);
            return true;
        }

        if (HandleSmoothnessMinMaxProperty(name, description, property, "_Smoothness"))
            return true;

        if (HandleSmoothnessMinMaxProperty(name, description, property, "_SecondSmoothness"))
            return true;

        if (IsSpecificProperty(shaderEffectControlPropertyName, 0) && name.StartsWith(shaderEffectKeyWord))
            return true;
        return false;
    }

    private bool IsMaterialEffectEnable(string propertyName, string effectName)
    {
        var controlProperty = FindProperty(effectName, currentProps, false);
        if (controlProperty != null && controlProperty.floatValue == 0 && propertyName.StartsWith(effectName) && effectName != propertyName)
            return false;
        return true;
    }

    public bool IsSpecificProperty(string controlPropertyName, float value)
    {
        var controlProperty = FindProperty(controlPropertyName, currentProps, false);
        return controlProperty != null && controlProperty.floatValue == value;
    }

    public void HandleProperty(string name, string description, MaterialProperty property)
    {
        var enable = true;
        foreach(var effect in shaderEffects)
        {
            enable &= IsMaterialEffectEnable(name, effect);
        }
        if (enable)
            currentMaterialEditor.ShaderProperty(property, description);
    }

    const string remapingMinName = "RemapMin";
    const string remapingMaxName = "RemapMax";
    const string remapingFeatureName = "Remapping";

    

    public bool HandleSmoothnessMinMaxProperty(string name, string description, MaterialProperty property, string featureName)
    {
        var minName = featureName + remapingMinName;
        var maxName = featureName + remapingMaxName;
        if (name.Contains(minName))
        {
            var maxProperty = FindProperty(maxName, currentProps, false);
            float min, max;
            min = property.floatValue;
            max = maxProperty.floatValue;
            EditorGUI.BeginChangeCheck();
            EditorGUILayout.MinMaxSlider(featureName + " " + remapingFeatureName, ref min, ref max, 0, 1);
            if (EditorGUI.EndChangeCheck())
            {
                property.floatValue = min;
                maxProperty.floatValue = max;
            }
            return true;
        }
        if (name.Contains(maxName))
            return true;
        return false;
    }

    private void ShowRainEffectParam(MaterialProperty property)
    {
        EditorGUI.BeginChangeCheck();
        var vec = Vector4.zero;
        vec.x = EditorGUILayout.Slider("Rain Metallic Noise Factor", property.vectorValue.x, 0.0f, 5.0f);
        vec.y = EditorGUILayout.Slider("Rain Smoothness Noise Factor", property.vectorValue.y, 0.0f, 5.0f);
        vec.z = EditorGUILayout.Slider("Rain Wet Flow Factor", property.vectorValue.z, 0.0f, 1.0f);
        vec.w = EditorGUILayout.Slider("Rain Noise Threshold", property.vectorValue.w, 0.01f, 0.99f);
        if (EditorGUI.EndChangeCheck())
        {
            property.vectorValue = vec;
        }
    }

    private GUIStyle headStyle = new GUIStyle();
    private void ShowIndirectLightingParam(MaterialProperty property)
    {
        headStyle.fontStyle = FontStyle.Bold;
        EditorGUILayout.Space();
        EditorGUILayout.Space();
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("Indirect Lighting", headStyle);
        EditorGUI.BeginChangeCheck();
        var vec = Vector4.zero;
        vec.x = EditorGUILayout.Slider("Total Indirect Diffuse Intensity", property.vectorValue.x, 0.0f, 2.0f);
        vec.y = EditorGUILayout.Slider("Backface Add Light Intensity", property.vectorValue.y, 0.0f, 0.5f);
        vec.z = EditorGUILayout.Slider("Indirect Light NormalMap Intensity", property.vectorValue.z, 0.0f, 1.0f);
        vec.w = EditorGUILayout.Slider("Indirect YDir Control", property.vectorValue.w, 0.0f, 1.0f);
        if (EditorGUI.EndChangeCheck())
        {
            property.vectorValue = vec;
        }
    }

    private void ShowRimLightingParam(MaterialProperty property)
    {
        EditorGUI.BeginChangeCheck();
        var vec = Vector4.zero;
        vec.x = EditorGUILayout.Slider("Rim Light Offset", property.vectorValue.x, -1.0f, 1.0f);
        vec.y = EditorGUILayout.Slider("Rim View Offset", property.vectorValue.y, -1.0f, 1.0f);
        vec.z = EditorGUILayout.Slider("Rim Shadow Control", property.vectorValue.z, 0.0f, 1.0f);
        vec.w = EditorGUILayout.Slider("Rim YDir Control", property.vectorValue.w, 0.0f, 1.0f);
        if (EditorGUI.EndChangeCheck())
        {
            property.vectorValue = vec;
        }
    }

    public void ShowBlendMode(MaterialProperty blendMode, BlendMode minMode = BlendMode.Opaque, BlendMode maxMode = BlendMode.Transparent)
    {
        EditorGUI.showMixedValue = blendMode.hasMixedValue;
        var mode = (BlendMode)blendMode.floatValue;

        EditorGUI.BeginChangeCheck();
        int temp = EditorGUILayout.Popup("Rendering Mode", (int)mode, blendNames);
        mode = (BlendMode)Mathf.Clamp(temp, (int)minMode, (int)maxMode);
        if (EditorGUI.EndChangeCheck())
        {
            currentMaterialEditor.RegisterPropertyChangeUndo("Rendering Mode");
            blendMode.floatValue = (float)mode;
            SetupMaterialWithBlendMode(currentMaterial, mode);
        }

        EditorGUI.showMixedValue = false;
    }

    public static void SetupMaterialWithBlendMode(Material material, BlendMode blendMode)
    {
        switch (blendMode)
        {
            case BlendMode.Opaque:
                material.SetOverrideTag("RenderType", "");
                material.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.One);
                material.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.Zero);
                material.SetInt("_ZWrite", 1);
                material.DisableKeyword("_ALPHATEST_ON");
                material.DisableKeyword("_ALPHABLEND_ON");
                material.DisableKeyword("_ALPHAPREMULTIPLY_ON");
                material.renderQueue = -1;
                break;
            case BlendMode.Cutout:
                material.SetOverrideTag("RenderType", "TransparentCutout");
                material.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.One);
                material.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.Zero);
                material.SetInt("_ZWrite", 1);
                material.EnableKeyword("_ALPHATEST_ON");
                material.DisableKeyword("_ALPHABLEND_ON");
                material.DisableKeyword("_ALPHAPREMULTIPLY_ON");
                material.renderQueue = (int)UnityEngine.Rendering.RenderQueue.AlphaTest;
                break;
            case BlendMode.Fade:
                material.SetOverrideTag("RenderType", "Transparent");
                material.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.SrcAlpha);
                material.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha);
                material.SetInt("_ZWrite", 0);
                material.DisableKeyword("_ALPHATEST_ON");
                material.EnableKeyword("_ALPHABLEND_ON");
                material.DisableKeyword("_ALPHAPREMULTIPLY_ON");
                material.renderQueue = (int)UnityEngine.Rendering.RenderQueue.Transparent;
                break;
            case BlendMode.Transparent:
                material.SetOverrideTag("RenderType", "Transparent");
                material.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.One);
                material.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha);
                material.SetInt("_ZWrite", 0);
                material.DisableKeyword("_ALPHATEST_ON");
                material.DisableKeyword("_ALPHABLEND_ON");
                material.EnableKeyword("_ALPHAPREMULTIPLY_ON");
                material.renderQueue = (int)UnityEngine.Rendering.RenderQueue.Transparent;
                break;
        }
    }

    public void ShowShaderKeyword()
    {
        showKeyword = GUILayout.Toggle(showKeyword, "ShowKeyword");
        if (showKeyword == false || currentMaterial == null)
            return;

        var keywords = currentMaterial.shaderKeywords;
        foreach(var key in keywords)
        {
            GUILayout.BeginHorizontal();
            if (GUILayout.Button(key))
            {
                currentMaterial.DisableKeyword(key);
            }
            GUILayout.EndHorizontal();
        }
    }
}
