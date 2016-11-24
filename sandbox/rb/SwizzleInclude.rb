def passing(criteria, feedback)
  puts "<PASS::>" + criteria
  if !feedback.nil?
    puts "<FEEDBACK::>" + feedback
  end
end

def failing(criteria, feedback)
  puts "<FAIL::>" + criteria
  if !feedback.nil?
    puts "<FEEDBACK::>" + feedback
  end
end
