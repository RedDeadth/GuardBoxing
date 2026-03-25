export default class Locker {
    constructor({ id, location, blocked, occupied, open, userId, userEmail, userName }) {
        this.id = id;
        this.location = location;
        this.blocked = blocked;
        this.occupied = occupied;
        this.open = open;
        this.userId = userId;
        this.userEmail = userEmail;
        this.userName = userName;
    }
    isBlocked() { return this.blocked; }
    isOpen() { return this.open; }
    isOccupied() { return this.occupied; }
}
