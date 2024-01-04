def generate_custom_number_column_with_2_to_8(start_prefix, start_number, end_number, leading_zeros=3):
    """
    Generates a formatted column of numbers with a specified prefix, including numbers ending with 2 through 8.

    Parameters:
    - start_prefix: The prefix for the starting number.
    - start_number: The starting value of the range.
    - end_number: The ending value of the range.
    - leading_zeros: The number of leading zeros in the formatted numbers.

    Returns:
    - A string with formatted numbers in a column.
    """
    formatted_numbers = []

    for i in range(start_number, end_number + 1):
        last_digit = i % 10
        if 2 <= last_digit <= 8:
            formatted_number = f"{start_prefix}-{str(i).zfill(leading_zeros)};"
            formatted_numbers.append(formatted_number)

    formatted_column = "\n".join(formatted_numbers)
    return formatted_column

# Example usage:
start_prefix_value = "10"
start_number_value = 11
end_number_value = 719
leading_zeros_value = 3

result_column = generate_custom_number_column_with_2_to_8(start_prefix_value, start_number_value, end_number_value, leading_zeros_value)
print("Generated Custom Number Column with 2 to 8:")
print(result_column)
