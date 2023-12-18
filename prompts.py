sequence_steps_example = """ Breakdown the text into sequence steps: For christmas shopping, we need first need to have some money. Then we go shopping, and then think what we want to buy. The things we can buy are iPhone, car or laptop.
          The sequence steps are as follows:
          1. Start
          2. Christmas Festival
          3. Have Some Money
          4. If Yes Go shopping
          5. If No Ends
          6. Go Shopping
          7. Think What to Buy
          8. If One Laptop
          9. If Two IPhone
          10. If Three Car.
          11. End""".strip()

mermaid_code_example = """Generate a flowchart mermaid code for the above sequence steps.
          The mermaid code for the above text is as follows:
          graph TD
            Start((Start)) --> A[Christmas Festival]
            A --> B{Have Some Money} 
            B --> |Yes| C(Go shopping)
            B --> |No| End((End))
            C --> D{Think What to Buy}
            D --> |One| E[Laptop] 
            D --> |Two| F[iPhone] 
            D --> |Three| G[fa:fa-car Car]""".strip()

input_text_example1 = "I check the time whether it is morning, afternoon and evening. If it morning I need to have breakfast. If it is afternoon i need to have lunch. If it is evening i need to have a tea."
input_text_example2 = "We are feeling hungry and we thought to eat dosa, pizza, and biryani.  We decided to head to a pizza shop, placed our order for a delicious pizza, and thoroughly enjoyed our meal."