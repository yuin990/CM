using UnityEngine;
using UnityEngine.SceneManagement;

public class MainMenu : MonoBehaviour
{
    public void OnPlayButton()
    {
        SceneManager.LoadScene("GameScene"); // 게임 씬 이름
    }

    public void OnQuitButton()
    {
        Application.Quit(); // 빌드된 게임에서만 작동
    }
}

