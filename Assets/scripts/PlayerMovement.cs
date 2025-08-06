using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public float moveSpeed = 5.0f;

    private Rigidbody2D rb;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        if (rb == null)
        {
            Debug.LogError("PlayerMovement 스크립트에는 Rigidbody2D 컴포넌트가 필요합니다!");
        }
    }

    void FixedUpdate()
    {
        float horizontalInput = Input.GetAxis("Horizontal");
        float verticalInput = Input.GetAxis("Vertical");

        Vector2 moveInput = new Vector2(horizontalInput, verticalInput).normalized;

        rb.linearVelocity = moveInput * moveSpeed;
    }
}