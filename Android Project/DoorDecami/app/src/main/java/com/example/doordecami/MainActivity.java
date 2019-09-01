package com.example.doordecami;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.ImageView;
import android.widget.TextView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class MainActivity extends AppCompatActivity {

    FirebaseDatabase database;
    DatabaseReference door_state_ref;

    ImageView image_door_state;
    TextView text_door_state;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //View 가져오기
        image_door_state = findViewById(R.id.imageView_state);
        text_door_state = findViewById(R.id.textView_state);

        //Firebase 설정
        database = FirebaseDatabase.getInstance();
        door_state_ref = database.getReference().child("door_state");
        door_state_ref.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                Boolean door_state = dataSnapshot.getValue(Boolean.class);
                if(door_state) {
                    image_door_state.setImageResource(R.drawable.open);
                    text_door_state.setText("문이 열렸습니다.");
                }
                else {
                    image_door_state.setImageResource(R.drawable.closed);
                    text_door_state.setText("문이 닫혔습니다.");
                }

            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
    }
}
