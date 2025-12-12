class ITTicket:
    def __init__(self, ticket_id: int, priority: str, description: str, status: str, assigned_to: str, created_at: str, resolution_time_hours: int):
        self.ticket_id = ticket_id
        self.priority = priority
        self.description = description
        self.status = status
        self.assigned_to = assigned_to
        self.created_at = created_at
        self.resolution_time_hours = resolution_time_hours

    def get_id(self):
        return self.ticket_id

    def get_priority(self):
        return self.priority

    def get_description(self):
        return self.description

    def get_status(self):
        return self.status

    def get_assigned_to(self):
        return self.assigned_to

    def get_created_at(self):
        return self.created_at

    def get_resolution_time(self):
        return self.resolution_time_hours
