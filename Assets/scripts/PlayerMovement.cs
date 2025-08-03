using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public Vector2 minBounds;
    public Vector2 maxBounds;

    public float moveSpeed = 5f;

    private Rigidbody2D rb;
    private Vector2 movement;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        void Start()
        {
            rb = GetComponent<Rigidbody2D>();

            // 카메라 기준 화면 범위를 가져와서 자동 설정
            Vector3 screenBottomLeft = Camera.main.ViewportToWorldPoint(new Vector3(0, 0, 0));
            Vector3 screenTopRight = Camera.main.ViewportToWorldPoint(new Vector3(1, 1, 0));

            minBounds = new Vector2(screenBottomLeft.x, screenBottomLeft.y);
            maxBounds = new Vector2(screenTopRight.x, screenTopRight.y);
        }
    }

    void Update()
    {
        movement.x = Input.GetAxisRaw("Horizontal");
        movement.y = Input.GetAxisRaw("Vertical");
    }

    void FixedUpdate()
    {
        Vector2 newPos = rb.position + movement * moveSpeed * Time.fixedDeltaTime;

        // 배경 범위 안에만 이동
        newPos.x = Mathf.Clamp(newPos.x, minBounds.x, maxBounds.x);
        newPos.y = Mathf.Clamp(newPos.y, minBounds.y, maxBounds.y);

        rb.MovePosition(newPos);
    }
}
