using UnityEngine;
using UnityEngine.SceneManagement;

public class MainMenu : MonoBehaviour
{
    public void OnPlayButton()
    {
        SceneManager.LoadScene("GameScene"); // ���� �� �̸�
    }

    public void OnQuitButton()
    {
        Application.Quit(); // ����� ���ӿ����� �۵�
    }
}

